import os

# =============================
# Paths
# =============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "db")

# =============================
# Embedding Model
# =============================

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
# =============================
# LLM Model
# =============================

LLM_MODEL_NAME = "llama3.1"


# =============================
# Text Splitter
# =============================

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

# =============================
# Retriever
# =============================

RETRIEVER_K = 4