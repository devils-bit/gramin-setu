import os
import sys

# Fix for Windows Unicode output issues
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

import time
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()


try:
    import sounddevice as sd
    import scipy.io.wavfile as wav
except ImportError:
    print("Missing audio libraries. Please install them via: pip install sounddevice scipy")
    sys.exit(1)

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from app.services.stt_handler import stt_handler
from app.services.gemini_handler import detect_and_respond
from app.services.tts_engine import tts_engine

def record_audio(filename, record_seconds=6):
    rate = 16000
    print(f"\n🎤 [AI-PCO Active] Listening into microphone for {record_seconds} seconds...")
    # Record audio using sounddevice
    recording = sd.rec(int(record_seconds * rate), samplerate=rate, channels=1, dtype='int16')
    sd.wait() # wait until recording is finished
    print("✅ Recording complete. Processing audio...")
    
    # Save as WAV file
    wav.write(filename, rate, recording)

def play_audio(filename):
    print("🔊 Playing out response over speaker...")
    # Use OS default music player based on the platform
    if os.name == 'nt':
        os.system(f'start {filename}') # Windows
    elif sys.platform == 'darwin':
        os.system(f'afplay {filename}') # macOS
    else:
        os.system(f'mpg123 {filename}') # Linux
    time.sleep(1)

def run_pco():
    print("="*60)
    print(" 🏛️ Gramin-Setu AI-PCO (Voice Box) is Online ".center(60))
    print("="*60)
    print("This mode simulates a Smart Speaker placed at a Gram Panchayat.")
    print("Press Enter to start interacting, or Ctrl+C to exit.\n")
    
    os.makedirs("recordings", exist_ok=True)
    os.makedirs("responses", exist_ok=True)
    
    while True:
        try:
            input("👉 Press [ENTER] to Speak:")
            wav_path = f"recordings/pco_input.wav"
            
            record_audio(wav_path, record_seconds=6)
            
            # STT Processing
            print("⏳ [1/3] Converting Speech to Text (Bhashini/Whisper)...")
            result = stt_handler.transcribe(wav_path)
            transcription = result[0] if isinstance(result, tuple) else result
            print(f"\n👤 Farmer Query: '{transcription}'")

            print("⏳ [2/3] Detecting language & querying Gemini...")
            answer, lang = detect_and_respond(transcription)
            print(f"🌍 Detected Language: {lang}")
            print(f"🤖 Answer: '{answer}'\n")

            # TTS Output
            print("⏳ [3/3] Synthesizing Voice Output...")
            response_audio = tts_engine.generate_audio(answer, "pco_response.mp3", lang=lang)
            
            # Audio Playback
            play_audio(str(Path("responses") / "pco_response.mp3"))
            
        except KeyboardInterrupt:
            print("\n❌ AI-PCO Shutting Down.")
            break
        except Exception as e:
            print(f"\n⚠️ System Error: {e}")

if __name__ == "__main__":
    run_pco()
