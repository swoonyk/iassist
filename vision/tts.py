import torch
import logging
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

    def process_message(self, message: str, priority: int):
        """Process a single message with priority."""
        try:
            # Interrupt lower priority messages
            if priority > self.current_priority:
                sd.stop()

            self.current_priority = priority
            generator = self.pipeline(message, voice=self.voice, speed=1.0)
            
            for _, _, audio in generator:
                if not self.is_running:
                    break
                sd.play(audio, samplerate=24000)
                sd.wait()

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
            # Process messages from navigation queue
            if nav_queue.queue:
                message, priority = nav_queue.queue[0]
                tts_processor.add_message(message, priority)
                nav_queue.queue.pop(0)
            
    except KeyboardInterrupt:
        logger.info("Stopping TTS processor...")
        tts_processor.stop()

if __name__ == "__main__":
    main()