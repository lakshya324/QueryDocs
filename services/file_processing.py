from PyPDF2 import PdfReader
from config.config_env import CHUNK_SIZE
from fastapi import UploadFile

def extract_text(file: UploadFile) -> str:
    """
    Extract text from an uploaded file (supports PDF and plain text).
    """
    if file.filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif file.filename.endswith(".txt"):
        return file.file.read().decode("utf-8")
    else:
        raise Exception("Unsupported file type. Please upload a PDF or text file.")


def chunk_text(text: str) -> list[str]:
    """
    Split text into smaller chunks for vectorization.
    """
    words = text.split()
    chunks = [" ".join(words[i : i + CHUNK_SIZE]) for i in range(0, len(words), CHUNK_SIZE)]
    return chunks
