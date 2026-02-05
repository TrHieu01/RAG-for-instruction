![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.53+-red?style=flat-square&logo=streamlit)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-green?style=flat-square)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-crimson?style=flat-square)

---

- **Frontend**: Streamlit (Custom CSS)
- **LLM**: Ollama + Qwen 2.5:14b
- **Embeddings**: BAAI/bge-m3 (1024 dims)
- **Reranker**: BAAI/bge-reranker-v2-m3
- **Vector DB**: Qdrant (Local persistent)
- **Memory**: Custom Mem0 implementation


### Yêu cầu
- **Ollama** đã được cài đặt và chạy

### Các bước cài đặt
   ```powershell
   uv sync
   ```
   *Hoặc pip:* `pip install -r requirements.txt`

**Tải Model cho Ollama**
   ```powershell
   ollama pull qwen2.5:14b
   ollama pull bge-m3
   ```

---

## 💻 Cách Chạy Ứng Dụng

1. **Khởi động Ollama Server**
   ```powershell
   ollama serve
   ```

2. **Chạy ứng dụng Streamlit**
   ```powershell
   uv run streamlit run app.py
   ```
   
3. **Truy cập**: Mở trình duyệt tại `http://localhost:8501`

```python
# Cấu hình LLM
LLM_MODEL_NAME = "qwen2.5:14b"    # Đổi sang "qwen2.5:7b" nếu máy yếu
LLM_TEMP = 0.1                    # Độ sáng tạo (thấp = chính xác hơn)

# Cấu hình Chunking (Quan trọng cho hiệu năng ingestion)
CHUNK_SIZE = 1000                 # Kích thước mỗi đoạn văn bản
CHUNK_OVERLAP = 200               # Độ chồng lặp để giữ ngữ cảnh



