import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "enterprise_knowledge")

CHAT_MODEL = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
