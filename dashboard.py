import sys

# Fix for Windows Unicode output issues
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

import streamlit as st
import json
from pathlib import Path

# Add project root to path so we can import 'app' module
import sys
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from app.services.rag_handler import rag_handler

st.set_page_config(page_title="Antyodaya Admin Dashboard", layout="wide", page_icon="🏛️")

LOG_FILE = BASE_DIR / "data" / "call_logs.json"
DATA_DIR = BASE_DIR / "data"

st.title("🏛️ Antyodaya Semantic Engine - Admin Dashboard")
st.markdown("Live monitoring of farmer queries and knowledge base management.")

# Sidebar for controls
with st.sidebar:
    st.header("🗄️ Knowledge Base")
    st.write("Manage the automated RAG pipeline here.")
    
    if st.button("🔄 Trigger Re-ingestion", use_container_width=True):
        with st.spinner("Ingesting PDFs from /data..."):
            pdf_files = list(DATA_DIR.glob("*.pdf"))
            if not pdf_files:
                st.warning(f"No PDF files found in {DATA_DIR.name}/")
            else:
                total_chunks = 0
                for pdf_path in pdf_files:
                    try:
                        chunks = rag_handler.process_pdf(str(pdf_path))
                        total_chunks += chunks
                    except Exception as e:
                        st.error(f"Failed parsing {pdf_path.name}: {e}")
                st.success(f"Successfully processed {len(pdf_files)} schemes into {total_chunks} vector chunks!")

st.header("📞 Live Voice Call Logs")

if LOG_FILE.exists():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
            
        if not logs:
            st.info("No calls logged yet.")
        else:
            # Display logs in reverse chronological order
            for log in reversed(logs):
                # We use expander to make it clean
                lang_code = log.get('language', 'hi')
                with st.expander(f"📞 Time: {log.get('timestamp', 'Unknown')} | Lang: {lang_code.upper()} | Status: Resolved"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**User Transcription:**")
                        st.info(log.get('transcription', ''))
                        
                        st.markdown("**Answers Generated:**")
                        st.success(log.get('answer', ''))
                        
                    with col2:
                        st.markdown("**Retrieved Document Context (RAG):**")
                        context = log.get('rag_context', '')
                        if context:
                            st.warning(context)
                        else:
                            st.write("*No exact factual reference matched in vector store.*")

    except Exception as e:
        st.error(f"Error reading logs: {e}")
else:
    st.info("No system activity tracked yet. Awaiting live incoming voice queries.")
