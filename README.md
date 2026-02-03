
> **Trợ lý Tài liệu Thông minh** được hỗ trợ bởi RAG (Retrieval-Augmented Generation) Tiên tiến.

Một ứng dụng chatbot RAG hiệu năng cao, cho phép bạn trò chuyện với các tài liệu PDF/DOCX của mình bằng cách sử dụng LLM cục bộ (Local LLM). Được xây dựng với giao diện Glassmorphism tuyệt đẹp và bộ nhớ dài hạn.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.53+-red?style=flat-square&logo=streamlit)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-green?style=flat-square)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-crimson?style=flat-square)

---

## ✨ Tính Năng Nổi Bật

| Tính năng | Mô tả |
|---------|-------------|
| 📄 **Xử lý Tài liệu Thông minh** | Sử dụng **Docling** để chuyển đổi PDF/DOCX sang Markdown cấu trúc cao. |
| ✂️ **Phân mảnh Tối ưu** | Kết hợp phân mảnh theo Header và Recursive để bảo toàn ngữ cảnh tốt nhất. |
| 🔍 **Tìm kiếm Tiên tiến** | Hybrid Search (BM25 + Vector) với **BGE-M3** embeddings và Reranker v2. |
| 🧠 **Bộ nhớ Dài hạn** | Hệ thống nhớ **Mem0** giúp AI nhớ tên và sở thích của bạn qua các phiên làm việc. |
| ⚡ **Hiệu năng Cao** | Pipeline ingestion được tối ưu hóa, hỗ trợ xử lý file lớn (1000+ trang). |
| 🎨 **Giao diện Premium** | Thiết kế Glassmorphism hiện đại, mượt mà với các hiệu ứng động. |
| 🛠️ **Quản lý File** | Giao diện quản lý file đã ingest, hiển thị tên file gốc chính xác. |

---

## 🛠️ Công Nghệ Sử Dụng

```mermaid
graph TD
    User[Tuy Nguyen] --> UI[Streamlit UI]
    UI --> Ingestion[Ingestion Pipeline]
    UI --> Query[Query Pipeline]
    
    subgraph "Ingestion (Xử lý dữ liệu)"
        Ingestion --> Docling[Docling Parser]
        Docling --> Chunking[Smart Chunking]
        Chunking --> Embed[BGE-M3 Embedding]
        Embed --> VectorDB[(Qdrant DB)]
    end
    
    subgraph "Query (Truy vấn)"
        Query --> Retriever[Hybrid Retriever]
        Retriever --> Reranker[BGE-Reranker]
        Reranker --> LLM[Ollama (Qwen 2.5)]
        LLM --> Memory[User Memory]
    end
```

- **Frontend**: Streamlit (Custom CSS)
- **LLM**: Ollama + Qwen 2.5:14b
- **Embeddings**: BAAI/bge-m3 (1024 dims)
- **Reranker**: BAAI/bge-reranker-v2-m3
- **Vector DB**: Qdrant (Local persistent)
- **Memory**: Custom Mem0 implementation

---

## 🚀 Hướng Dẫn Cài Đặt

### Yêu cầu
- **Python 3.10+** (Khuyên dùng 3.11 hoặc 3.12)
- **Ollama** đã được cài đặt và chạy
- **RAM**: 8GB+ (Khuyên dùng 16GB cho model 14b)

### Các bước cài đặt

1. **Clone dự án**
   ```powershell
   git clone <repo-url>
   cd antigravity-rag
   ```

2. **Cài đặt thư viện (sử dụng `uv` cho nhanh)**
   ```powershell
   uv sync
   ```
   *Hoặc pip:* `pip install -r requirements.txt`

3. **Tải Model cho Ollama**
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

---

## ⚙️ Cấu Hình (`src/config.py`)

Bạn có thể tùy chỉnh các thông số trong file `src/config.py`:

```python
# Cấu hình LLM
LLM_MODEL_NAME = "qwen2.5:14b"    # Đổi sang "qwen2.5:7b" nếu máy yếu
LLM_TEMP = 0.1                    # Độ sáng tạo (thấp = chính xác hơn)

# Cấu hình Chunking (Quan trọng cho hiệu năng ingestion)
CHUNK_SIZE = 1000                 # Kích thước mỗi đoạn văn bản
CHUNK_OVERLAP = 200               # Độ chồng lặp để giữ ngữ cảnh
```

---




---

---

## 🤝 Đóng Góp

Dự án được phát triển với tinh thần mã nguồn mở. Mọi đóng góp đều được hoan nghênh!

---
<p align="center">
  Made with ❤️ by <strong>Antigravity Team</strong>
</p>


