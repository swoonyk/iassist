import os
import pyaudio
import wave
from datetime import datetime
from groq import Groq
import time
from dotenv import load_dotenv

# Setup directories
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "recordings")
os.makedirs(AUDIO_DIR, exist_ok=True)
load_dotenv()

def check_microphone_permission():
    """Check and request microphone permissions"""
    try:
        # Try to initialize audio
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )
        stream.stop_stream()
        stream.close()
        p.terminate()
        return True
    except OSError:
        # Prompt for permissions
        print("Microphone access needed. Opening System Preferences...")
        subprocess.run([
            "open",
            "x-apple.systempreferences:com.apple.preference.security?Privacy_Microphone"
        ])
        input("Press Enter after granting permission...")
        return False


def record_audio(duration=5):
    """Record audio for specified duration and save to file"""

    if not check_microphone_permission():
        print("Please restart the application after granting permission")
        return None

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                   channels=CHANNELS,
                   rate=RATE,
                   input=True,
                   frames_per_buffer=CHUNK)

    print("* recording")
    frames = []

    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(AUDIO_DIR, f"recording_{timestamp}.wav")

    # Save the recorded audio
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename

def transcribe_file(filename):
    """Transcribe audio file using Groq"""
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )
    
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()),
            model="whisper-large-v3-turbo",
            response_format="json",
            language="en",
            temperature=0.0
        )
        return transcription.text

if __name__ == "__main__":
    try:
        # Record audio
        print("Starting recording...")
        audio_file = record_audio(duration=5)
        if audio_file:
          print(f"Audio saved to: {audio_file}")
        
        # Transcribe
        print("Transcribing...")
        text = transcribe_file(audio_file)
        print("Transcription:", text)
        
    except Exception as e:
        print(f"Error: {str(e)}")