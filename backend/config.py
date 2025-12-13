import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set. Please set it in your environment or .env file.")

# Model names (you can swap these to what your account supports)
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4.1-mini"  # or gpt-4.1 / gpt-4o etc.

# Paths
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
SYNTHETIC_DATA_DIR = BASE_DIR / "data" / "synthetic"
VECTOR_DB_DIR = BASE_DIR / "vector_store" / "chroma"

# RAG configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 5
MIN_SIMILARITY_SCORE = 0.3  # rough heuristic
