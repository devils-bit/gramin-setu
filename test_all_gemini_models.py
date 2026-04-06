import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Set encoding for Windows terminal
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

def test_all_models():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not found in .env")
        return
    
    genai.configure(api_key=api_key)
    
    print("Listing models and testing generate_content...")
    try:
        models = genai.list_models()
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                print(f"Testing model: {m.name}...", end=" ", flush=True)
                try:
                    model = genai.GenerativeModel(m.name)
                    response = model.generate_content("Hi")
                    print(f"SUCCESS: {response.text.strip()}")
                except Exception as e:
                    print(f"FAILED: {e}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    test_all_models()
