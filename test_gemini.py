import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

# Fix for Windows Unicode output issues
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # Older Python versions fallback
        pass

# Load .env from specific path if needed, but here it's expected in current dir or parent
load_dotenv()

def test_raw_genai():
    print("Testing raw google-generativeai...")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[-] GEMINI_API_KEY not found in .env")
        return
    
    genai.configure(api_key=api_key)
    # Using 'models/' prefix can sometimes help if the short name fails
    names_to_try = [
        "gemini-3-flash-preview", 
        "gemini-3.1-flash-lite-preview",
        "gemini-2.5-flash", 
        "gemini-2.0-flash", 
        "gemini-1.5-flash", 
        "gemini-1.5-flash-latest", 
        "gemini-flash-latest",
        "models/gemini-1.5-flash"
    ]
    
    for model_name in names_to_try:
        try:
            print(f"Trying {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say hello in Hindi")
            print(f"[SUCCESS] Raw GenAI ({model_name}) response: {response.text.strip()}")
            return # Success!
        except Exception as e:
            print(f"[FAILED] Raw GenAI ({model_name}) failed: {e}")

def test_langchain_genai():
    print("\nTesting langchain-google-genai...")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[-] GEMINI_API_KEY not found in .env")
        return
    
    # LangChain models typically use the name without the 'models/' prefix
    names_to_try = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-pro"]
    for model_name in names_to_try:
        try:
            print(f"Trying {model_name}...")
            llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
            response = llm.invoke("Say hello in Hindi")
            print(f"[SUCCESS] LangChain Gemini ({model_name}) response: {response.content.strip()}")
            return # Success!
        except Exception as e:
            print(f"[FAILED] LangChain Gemini ({model_name}) failed: {e}")

if __name__ == "__main__":
    test_raw_genai()
    test_langchain_genai()
