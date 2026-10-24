import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# App Directories
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
VECTORSTORE_DIR = DATA_DIR / "vectorstore"
DEMO_DIR = DATA_DIR / "demo_files"
DB_PATH = DATA_DIR / "studymind.db"

# Create required directories
for d in [DATA_DIR, UPLOADS_DIR, VECTORSTORE_DIR, DEMO_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()

# Model Configurations
DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "groq").lower()
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "qwen/qwen3.8-27b")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# RAG & Document Parameters
DEFAULT_CHUNK_SIZE = 600
DEFAULT_CHUNK_OVERLAP = 100
DEFAULT_TOP_K = 3
DEFAULT_TEMPERATURE = 0.2

# App Branding
APP_NAME = "StudyMind"
APP_TAGLINE = "Your AI-Powered Personal Learning Companion"
APP_VERSION = "1.0.0"
