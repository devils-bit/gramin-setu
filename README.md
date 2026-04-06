# Antyodaya Semantic Engine

A FastAPI project serving as the foundation for India Stack 2.0's Autonomous AI Agent layer. The Antyodaya Semantic Engine ingests government scheme PDFs into a ChromaDB vector store, preparing data for voice-native capabilities and agentic workflows.

## Features
- **Document Ingestion**: Automates PDF processing and RAG (Retrieval-Augmented Generation) setup.
- **Optimized for Bharat**: Configured textual chunking using `RecursiveCharacterTextSplitter` explicitly designed with script boundaries for Hindi (e.g., Devanagari Purna Viram `।`) and Telugu in mind.
- **Local Embeddings**: Operates offline utilizing `sentence-transformers/all-MiniLM-L6-v2`.
- **FastAPI**: Serves the semantic engine with high-performance routing.

## Getting Started

1. Set your working directory to the project folder:
   ```bash
   cd antyodaya_semantic_engine
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Folder Structure
- `app/main.py`: The entry point for FastAPI routes.
- `app/services/rag_handler.py`: Houses the `RAGHandler` class logic for ChromaDB integration and text chunking specific to targeted Indian languages.
- `data/`: Place your government scheme `*.pdf` files here.
- `chroma_db/`: Persistent local directory used by Chroma vector store.
