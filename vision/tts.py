import time
import torch
import logging
import numpy as np
from kokoro import KPipeline
import soundfile as sf
import sounddevice as sd
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Tuple
from .priority_list import NavigationQueue
import queue
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

##############################################
# NEW: Continuous Raw Playback using RawOutputStream
##############################################

# A high-resolution clock using time.monotonic_ns()
class Clock:
    def __init__(self) -> None:
        self._t0 = time.monotonic_ns()

    def get_time_ns(self) -> int:
        return time.monotonic_ns() - self._t0

# A Raw-stream based playback class that uses explicit blocksize and latency.
# This version uses sd.RawOutputStream so that the callback receives a raw bytes buffer.
class SoundSD_Raw:
    def __init__(self, data: np.ndarray, device: int, sample_rate: int,
                 blocksize: int = 256, latency: float = 0.005) -> None:
        """
        Parameters:
          data: NumPy array containing audio samples (mono or 2D with channels)
          device: output device index
          sample_rate: sampling frequency (Hz)
          blocksize: number of frames per callback (try 128 or 256)
          latency: desired latency (in seconds), e.g. 0.005 for ~5 ms
        """
        # Ensure data is 2D (columns = channels)
        self._data = data if data.ndim == 2 else data[:, np.newaxis]
        self._num_frames = self._data.shape[0]
        self._num_channels = self._data.shape[1]
        self._clock = Clock()
        self._current_frame = 0
        self._target_time = None

        # Open a RawOutputStream. Here we force a blocksize and low latency.
        self._stream = sd.RawOutputStream(
            blocksize=blocksize,
            callback=self._callback,
            channels=self._num_channels,
            device=device,
            dtype='float32',  # we assume our data is float32
            latency=latency,
            samplerate=sample_rate,
        )
        self._stream.start()

    def _callback(self, outdata, frames, time_info, status) -> None:
        """Raw stream callback.
        outdata is a writable bytes-like object.
        """
        if status:
            print(status)
        # If no target time is scheduled, fill with silence.
        if self._target_time is None:
            outdata[:] = b'\x00' * len(outdata)
            return

        # Calculate how many nanoseconds remain until the scheduled start.
        # time_info.outputBufferDacTime and time_info.currentTime are in seconds.
        delta_ns = int((time_info.outputBufferDacTime - time_info.currentTime) * 1e9)
        if self._clock.get_time_ns() + delta_ns < self._target_time:
            outdata[:] = b'\x00' * len(outdata)
            return

        end_frame = self._current_frame + frames
        if end_frame <= self._num_frames:
            chunk = self._data[self._current_frame:end_frame, :]
            self._current_frame += frames
        else:
            # When we've played all data, pad with zeros and stop scheduling.
            remaining = self._num_frames - self._current_frame
            chunk = self._data[self._current_frame:, :]
            pad = np.zeros((frames - remaining, self._num_channels), dtype=np.float32)
            chunk = np.vstack((chunk, pad))
            self._current_frame = 0
            self._target_time = None

        # Convert the chunk to raw bytes (float32 native order).
        out_bytes = chunk.astype(np.float32).tobytes()
        outdata[:] = out_bytes

    def play(self, when: Optional[float] = None) -> None:
        """Schedule playback.
        
        Parameters:
          when: delay in seconds relative to now (e.g. 0.5 for 500 ms delay).
                If None, playback starts immediately.
        """
        current_ns = self._clock.get_time_ns()
        self._target_time = current_ns if when is None else current_ns + int(when * 1e9)

##############################################
# TTSProcessor using the above Raw Playback backend
##############################################

class TTSProcessor:
    def __init__(self):
        self.pipeline = self._initialize_pipeline()
        self.voice = 'af_sarah'
        self.message_queue = queue.Queue()
        self.is_running = True
        self.current_priority = 0

    def _initialize_pipeline(self) -> Optional[KPipeline]:
        try:
            return KPipeline(
                lang_code='a',
                device='cuda' if torch.cuda.is_available() else 'cpu',
                trf=False
            )
        except Exception as e:
            logger.error(f"Error initializing TTS pipeline: {e}")
            return None

    def _play_audio_continuous(self, full_audio: np.ndarray) -> None:
        """
        Play the full_audio continuously using our Raw stream backend.
        It uses explicit blocksize and latency to minimize gaps.
        """
        # Query default output device info.
        device_info = sd.query_devices(sd.default.device["output"])
        sample_rate = 24000  # using same rate as before
        # Create our Raw playback object.
        playback = SoundSD_Raw(
            full_audio, 
            device=device_info["index"],
            sample_rate=sample_rate,
            blocksize=256,   # you can tweak this value
            latency=0.005    # try latency between 0.003 and 0.010 seconds
        )
        # Schedule playback immediately.
        playback.play(when=0)
        # Wait for playback to finish.
        duration = full_audio.shape[0] / sample_rate
        time.sleep(duration + 0.1)  # add a small buffer

    def process_message(self, message: str, priority: int):
        """Process a single message with priority."""
        try:
            # Interrupt lower priority messages.
            if priority > self.current_priority:
                sd.stop()

            self.current_priority = priority
            generator = self.pipeline(message, voice=self.voice, speed=1.0)
            chunks = []
            for _, _, audio in generator:
                if not self.is_running:
                    break
                chunks.append(audio)
            if chunks:
                # Concatenate all generated chunks into a single array.
                full_audio = np.concatenate(chunks, axis=0)
                # Play the full audio continuously using our Raw stream approach.
                self._play_audio_continuous(full_audio)
        except Exception as e:
            logger.error(f"Error processing message: {e}")
        finally:
            self.current_priority = 0

    def start_processing_thread(self):
        """Start the message processing thread."""
        def process_queue():
            while self.is_running:
                try:
                    message, priority = self.message_queue.get(timeout=1)
                    self.process_message(message, priority)
                except queue.Empty:
                    continue
                except Exception as e:
                    logger.error(f"Error in processing thread: {e}")

        threading.Thread(target=process_queue, daemon=True).start()

    def add_message(self, message: str, priority: int):
        """Add a message to the queue."""
        self.message_queue.put((message, priority))

    def stop(self):
        """Stop the TTS processor."""
        self.is_running = False
        sd.stop()

def main():
    tts_processor = TTSProcessor()
    if tts_processor.pipeline is None:
        return

    nav_queue = NavigationQueue()
    tts_processor.start_processing_thread()

    try:
        while True:
            # Process messages from navigation queue.
            if nav_queue.queue:
                message, priority = nav_queue.queue[0]
                tts_processor.add_message(message, priority)
                nav_queue.queue.pop(0)
    except KeyboardInterrupt:
        logger.info("Stopping TTS processor...")
        tts_processor.stop()

if __name__ == "__main__":
    main()
