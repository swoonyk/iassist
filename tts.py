import torch
import logging
from kokoro import KPipeline
import soundfile as sf
import sounddevice as sd
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_pipeline() -> Optional[KPipeline]:
    """Initialize the KPipeline with proper error handling."""
    try:
        pipeline = KPipeline(
            lang_code='a',
            device='cuda' if torch.cuda.is_available() else 'cpu',
            trf=False
        )
        return pipeline
    except ImportError as e:
        logger.error(f"Error importing required modules: {e}")
        logger.error('Please install required packages:')
        logger.error('pip install "kokoro[all]" espeak-ng transformers torch torchaudio sounddevice soundfile')
        return None
    except Exception as e:
        logger.error(f"Error initializing KPipeline: {e}")
        return None

def process_text_chunk(chunk: str, index: int, pipeline: KPipeline, voice: str, speed: float = 1.0) -> None:
    """Process a chunk of text and generate audio."""
    try:
        generator = pipeline(chunk, voice=voice, speed=speed, split_pattern=r'\n+')
        for i, (gs, ps, audio) in enumerate(generator):
            logger.info(f"Processing chunk {index}, segment {i}")
            logger.debug(f"Graphemes: {gs}")
            logger.debug(f"Phonemes: {ps}")
            
            # Play the audio
            sd.play(audio, samplerate=24000)
            sd.wait()
            
            # Save the audio file
            output_file = f'chunk_{index}_segment_{i}.wav'
            sf.write(output_file, audio, 24000)
            logger.info(f"Saved audio to {output_file}")
    except Exception as e:
        logger.error(f"Error processing chunk {index}: {e}")

def main():
    # Initialize the pipeline
    pipeline = initialize_pipeline()
    if pipeline is None:
        return

    # Configuration
    text = """I'm i Assist! I'm a virtual assistant looking out for you! 
              There is a chair on the left so I recommend veering right."""
    voice_01 = 'af_sarah'
    
    # Clean and split the text
    text = ' '.join(text.split())  # Normalize whitespace
    text_chunks = text.split('. ')
    text_chunks = [chunk.strip() + '.' for chunk in text_chunks if chunk.strip()]

    logger.info(f"Processing {len(text_chunks)} text chunks")

    # Process chunks in parallel
    try:
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(process_text_chunk, chunk, idx, pipeline, voice_01)
                for idx, chunk in enumerate(text_chunks)
            ]

            # Wait for all futures to complete
            for future in futures:
                future.result()
                
        logger.info("Text-to-speech processing completed successfully")
    except Exception as e:
        logger.error(f"Error during parallel processing: {e}")

if __name__ == "__main__":
    main()