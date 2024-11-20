from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

#* FastAPI Configuration
UVICORN_APP = os.getenv("UVICORN_APP", "main:app")
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 8000))
RELOAD = os.getenv("RELOAD", "true").lower() == "true"

#* VertorDB Configuration [Qdrant]
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
VECTOR_QUERY_SIZE = int(os.getenv("VECTOR_QUERY_SIZE", 10))

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
QDRANT_API_KEY= os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "default")

#* Embedding Configuration [Sentence Transformers]
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

#* Bhashini API Configuration
BHASHINI_API_URL = os.getenv("BHASHINI_API_URL")
BHASHINI_API_KEY = os.getenv("BHASHINI_API_KEY")

#* LLM Configuration [Ollama Llama]
LLAMA_MODEL = os.getenv("LLAMA_MODEL", "llama3.2")