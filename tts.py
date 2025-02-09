import torch
import logging
import time
import sounddevice as sd
import numpy as np
from kokoro import KPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TTSEngine:
    def __init__(self):
        sd.default.device = 2  # Explicit speaker selection
        self.pipeline = KPipeline(
            lang_code='a',
            device='cpu',
            trf=False
        )
        
    def _synthesize(self, text: str) -> np.ndarray:
        """Direct synthesis without streaming"""
        audio_chunks = []
        for _, _, audio in self.pipeline(text, voice='af_sarah', speed=1.25):
            audio_chunks.append(audio)
        return np.concatenate(audio_chunks) if audio_chunks else np.array([])

    def speak(self, text: str):
        """Blocking playback with verification"""
        audio = self._synthesize(text)
        if audio.size == 0:
            logger.error("No audio generated")
            return
            
        logger.info(f"Playing {len(audio)/24000:.2f}s audio")
        sd.play(audio, samplerate=24000)
        sd.wait()

def main():
    engine = TTSEngine()
    
    # Verification tests
    engine.speak("bookshelf nearby, watch out") 
    engine.speak("person in front of you, proceed with caution")
    #time.sleep(1)
    engine.speak("dog running on the street, be careful")

if __name__ == "__main__":
    main()