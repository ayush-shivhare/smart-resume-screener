import os
from dotenv import load_dotenv
load_dotenv()

USE_OPENAI = os.getenv("USE_OPENAI", "false").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
DB_URL = os.getenv("DB_URL", "sqlite:///./resumes.db")
TOP_K = int(os.getenv("TOP_K", "10"))
