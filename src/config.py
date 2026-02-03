
import os

# Paths
DATA_DIR = "data"
DB_PATH = "./qdrant_db"

# Embedding
EMBEDDING_MODEL_NAME = "BAAI/bge-m3"
DEVICE = "cpu" # or cuda

# Chunking (optimized for large PDFs - 500+ pages)
CHUNK_SIZE = 1000      # Larger chunks = fewer embeddings to compute
CHUNK_OVERLAP = 200    # Good overlap for context preservation

# Retrieval
TOP_K_RETRIEVAL = 10
TOP_K_RERANK = 3

# LLM
LLM_MODEL_NAME = "qwen2.5:14b" # Ollama model name
LLM_TEMP = 0.1
BASE_URL = "http://localhost:11434"

# Qdrant
COLLECTION_NAME = "antigravity_rag"
