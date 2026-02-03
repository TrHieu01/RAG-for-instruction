# 🌌 Antigravity Vibe RAG

> **Intelligent Document Assistant** powered by Advanced RAG (Retrieval-Augmented Generation)

A modern, high-performance RAG chatbot that allows you to chat with your PDF/DOCX documents using local LLMs. Built with a beautiful glassmorphism UI and persistent memory.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.53+-red?style=flat-square&logo=streamlit)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-green?style=flat-square)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **Smart Document Processing** | Docling converts PDF/DOCX to structured Markdown |
| ✂️ **Optimized Chunking** | Header-aware + Recursive splitting for context preservation |
| 🔍 **Advanced Retrieval** | BGE-M3 embeddings + MMR search + BGE-Reranker-v2 |
| 🧠 **Persistent Memory** | Mem0 remembers user preferences across sessions |
| 💬 **Streaming Responses** | Real-time response generation with Qwen 2.5 |
| 🎨 **Premium UI** | Glassmorphism design with smooth animations |

---

## 🛠️ Tech Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    ANTIGRAVITY RAG STACK                     │
├─────────────────────────────────────────────────────────────┤
│  Frontend:    Streamlit (Glassmorphism UI)                  │
│  LLM:         Ollama + Qwen 2.5:14b                         │
│  Embeddings:  BAAI/bge-m3 (1024 dims)                       │
│  Reranker:    BAAI/bge-reranker-v2-m3                       │
│  Vector DB:   Qdrant (local persistent)                     │
│  Memory:      Mem0 (user context)                           │
│  Doc Parser:  Docling (PDF/DOCX → Markdown)                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Ollama** installed and running
- **8GB+ RAM** (16GB recommended for 14b model)

### Installation

```powershell
# 1. Clone or navigate to project
cd c:\Users\Admin\Desktop\TrHius\1

# 2. Install dependencies with uv
uv sync

# 3. Pull the LLM model
ollama pull qwen2.5:14b

# 4. (Optional) Use smaller model if low on resources
ollama pull qwen2.5:7b
```

### Running the App

```powershell
# Start Ollama server (in a separate terminal)
ollama serve

# Run the application
uv run streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## 📁 Project Structure

```
antigravity-rag/
├── app.py                 # Main Streamlit application
├── pyproject.toml         # Dependencies
├── uv.lock                # Lock file
├── README.md              # This file
│
├── src/                   # Source code
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── ingestion.py       # Document processing pipeline
│   ├── retrieval.py       # Hybrid search + reranking
│   ├── llm.py             # LLM integration
│   ├── memory.py          # Mem0 user memory
│   ├── vector_db.py       # Qdrant vector store
│   └── utils.py           # Logging utilities
│
├── qdrant_db/             # Vector database storage
└── mem0_storage_v3/       # User memory storage
```

---

## ⚙️ Configuration

Edit `src/config.py` to customize:

```python
# LLM Settings
LLM_MODEL_NAME = "qwen2.5:14b"    # Change to "qwen2.5:7b" for lower resources
LLM_TEMP = 0.1                    # Lower = more focused responses

# Embedding
EMBEDDING_MODEL_NAME = "BAAI/bge-m3"
DEVICE = "cpu"                    # Change to "cuda" if you have NVIDIA GPU

# Chunking (for large PDFs)
CHUNK_SIZE = 1000                 # Characters per chunk
CHUNK_OVERLAP = 200               # Overlap between chunks

# Retrieval
TOP_K_RETRIEVAL = 10              # Documents to retrieve
TOP_K_RERANK = 3                  # Documents after reranking
```

---

## 📊 Performance

### Ingestion Speed (i7-14700F, CPU)

| PDF Size | Chunks | Time |
|----------|--------|------|
| 50 pages | ~100 | ~1-2 min |
| 200 pages | ~400 | ~4-6 min |
| 500 pages | ~900 | ~8-12 min |

### Tips for Better Performance

1. **Use GPU** - Set `DEVICE = "cuda"` for 10-20x faster embeddings
2. **Increase chunk size** - Fewer chunks = faster processing
3. **Use smaller LLM** - `qwen2.5:7b` is faster than `14b`

---

## 🧠 Memory System

The app remembers your preferences and past interactions using Mem0:

```
User: "My name is Hieu, I prefer Vietnamese"
Bot: "Nice to meet you, Hieu! I'll respond in Vietnamese from now on."

# After restart...

User: "What's my name?"
Bot: "Your name is Hieu, and you prefer Vietnamese responses!"
```

Memory is stored locally in `mem0_storage_v3/` and persists across restarts.

---

## 🔧 Troubleshooting

### "Connection refused" error
```powershell
# Ollama is not running. Start it:
ollama serve
```

### "File is being used by another process" error
```powershell
# Multiple Streamlit instances running. Kill them:
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force
```

### Slow ingestion
- Reduce `CHUNK_SIZE` in config
- Use GPU if available
- Close other applications

---

## 📝 License

MIT License - Feel free to use and modify!

---

## 🤝 Acknowledgments

- [Ollama](https://ollama.com/) - Local LLM runtime
- [Streamlit](https://streamlit.io/) - Web UI framework
- [LangChain](https://langchain.com/) - LLM orchestration
- [Qdrant](https://qdrant.tech/) - Vector database
- [Mem0](https://mem0.ai/) - Memory layer
- [Docling](https://github.com/DS4SD/docling) - Document parsing

---

<p align="center">
  Made with ❤️ by <strong>Antigravity Team</strong>
</p>



<!-- ollama run qwen2.5:14b -->
<!-- 2026-02-03 15:07:45,425 - src.ingestion - INFO - 💾 Vector store insertion: 1117.0s
2026-02-03 15:07:45,425 - src.ingestion - INFO - ✅ INGESTION COMPLETE: 1959 chunks in 3300.8s total -->