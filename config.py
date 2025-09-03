import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_DB_DIR = "data/chroma"

LLM_CONFIG = {
    "config_list": [
        {
            "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
            "api_key": GROQ_API_KEY,
            "base_url": "https://api.groq.com/openai/v1"
        }
    ],
    "cache_seed": 42,
}
