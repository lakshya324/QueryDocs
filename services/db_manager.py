import uuid
from qdrant_client.http.models import PointStruct
from config.config_qdrant import qdrant
from qdrant_client.models import Distance, VectorParams
from config.config_env import QDRANT_COLLECTION_NAME, VECTOR_QUERY_SIZE
from services.embedding import generate_embedding

# check if the collection exists otherwise create it
try:
    qdrant.get_collection(collection_name=QDRANT_COLLECTION_NAME)
except Exception:
    qdrant.create_collection(
        collection_name=QDRANT_COLLECTION_NAME,
        vectors_config=VectorParams(size=generate_embedding(["test"]).shape[-1], distance=Distance.COSINE),
    )


def add_document(chanks: list[str], vectors: list[list[float]]) -> dict:
    """
    Add a document to the Qdrant database.
    """
    if len(chanks) != len(vectors):
        raise ValueError("Number of chunks and vectors should be the same.")

    points = []
    doc_id = uuid.uuid4().hex
    chunks_ids = []
    for idx, vector in enumerate(vectors):
        id = uuid.uuid4().hex
        chunks_ids.append(id)
        points.append(
            PointStruct(
                id= id,
                vector=vector,
                payload={"content": chanks[idx], "doc_id": doc_id, "chunk_id": idx},
            )
        )
    qdrant.upsert(collection_name=QDRANT_COLLECTION_NAME, points=points)
    return {"doc_id": doc_id, "chunks_ids": chunks_ids}


def query_db(query_embedding: list[float]) -> list[str]:
    """
    Query the Qdrant database for similar vectors.
    """
    results = qdrant.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=query_embedding,
        limit=VECTOR_QUERY_SIZE,
    )

    return [
        result.payload["content"] for result in sorted(results, key=lambda x: x.score, reverse=True)
    ]


def delete_document(doc_id):
    """
    Delete all chunks of a document from the Qdrant database.
    """
    results = qdrant.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector={"payload.doc_id": doc_id},
        limit=1000,
    )

    qdrant.delete(collection_name=QDRANT_COLLECTION_NAME, ids=[result.id for result in results])
    