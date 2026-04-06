import os
import sys

# Fix for Windows Unicode output issues
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Load environment variables
load_dotenv()

from app.services.rag_handler import rag_handler

def main():
    print("="*60)
    print(" 📂 Antyodaya Data Ingestion System ".center(60))
    print("="*60)
    
    try:
        file_count, total_chunks = rag_handler.sync_data_directory()
        print(f"\n🚀 Success: {file_count} files indexed into ChromaDB.")
        print(f"📊 Total database chunks: {total_chunks}")
        print("\nYour project is now updated with the latest data!")
        
    except Exception as e:
        print(f"\n❌ Error during ingestion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
