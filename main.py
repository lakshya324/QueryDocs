import uvicorn
from fastapi import FastAPI, UploadFile, Form, HTTPException
from services.file_processing import extract_text, chunk_text
from services.translation import detect_language, translate
from services.embedding import generate_embedding
from services.db_manager import add_document, query_db, delete_document
from services.llm import prompt
from config.config_env import UVICORN_APP, PORT, RELOAD, HOST
from services.query_model import QueryRequest

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Document Search API!"}

@app.post("/upload")
async def upload_document(file: UploadFile):
    """
    Upload a document (PDF or text) and store it in chunks after processing.
    """
    try:
        # * Extract text from file (supports PDF and plain text)
        file_content = extract_text(file)
        
        print(file_content[:100])

        # * Detect language of whole document
        detected_language = detect_language(file_content)

        # * Chunk the text into smaller parts for vectorization
        chunks = chunk_text(file_content)

        # * Translate to English if necessary [Chunk by Chunk]
        if detected_language != "en":
            chunks = [translate(chunk) for chunk in chunks]

        # * Generate embeddings for each chunk
        embeddings = generate_embedding(chunks)

        # * Add chunks to the vector database [Qdrant]
        document = add_document(chunks, embeddings)
        doc_id = document["doc_id"]
        chunks_ids = document["chunks_ids"]
        

        return {
            "message": "Document uploaded successfully",
            "doc_id": doc_id,
            "chunks": {
                "count": len(chunks),
                "ids": chunks_ids,
            },
            "detected_language": detected_language,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def query_document(body: QueryRequest):
    """
    Query the database and return relevant results.
    """
    try:
        query = body.query
        
        # * Detect language of query
        detected_language = detect_language(query)

        # * Translate to English if necessary
        if detected_language != "en":
            query = translate(query)

        # * Generate embeddings for the query
        query_embedding = generate_embedding([query])[0]

        # * Query the database for similar vectors
        vectors = query_db(query_embedding)

        print(vectors)
        output = prompt(query, vectors)

        return {
            "message": "Query successful",
            "output": output,
            "detected_language": detected_language,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/delete")
async def delete_document_route(doc_id: str):
    """
    Delete a document by its ID.
    """
    try:
        delete_document(doc_id)
        return {"message": "Document deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(UVICORN_APP, host=HOST, port=PORT, reload=RELOAD)