from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from typing import List

# Initialize locally
try:
    # 1. Try to load from local cache first (Saves YOU from timeouts)
    encoder = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)
    print("🟢 Loaded SentenceTransformer from local cache.")
except Exception:
    # 2. If it fails, download it from HuggingFace (For the EVALUATOR)
    print("⏳ Model not found locally. Downloading from HuggingFace (this may take a minute)...")
    encoder = SentenceTransformer("all-MiniLM-L6-v2")
    print("🟢 Download complete.")

qdrant_client = QdrantClient(":memory:")
COLLECTION_NAME = "capstone_knowledge_base"

# Ensure collection exists on startup
qdrant_client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

def ingest_chunks(filename: str, chunks: List[str]):
    """Embeds text chunks and uploads them to Qdrant with metadata."""
    
    # We dynamically calculate IDs so we don't overwrite previous documents
    existing_count = qdrant_client.count(collection_name=COLLECTION_NAME).count
    
    points = []
    for i, chunk in enumerate(chunks):
        vector = encoder.encode(chunk).tolist()
        payload = {
            "filename": filename,
            "chunk_index": i,
            "text": chunk
        }
        point_id = existing_count + i
        points.append(PointStruct(id=point_id, vector=vector, payload=payload))

    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)
    return len(points)

def retrieve_context(query: str, top_k: int = 3) -> List[dict]:
    """Retrieves top-k relevant chunks. Returns empty list if DB is empty."""
    
    # Edge Case: User asks a question before uploading any documents
    if qdrant_client.count(collection_name=COLLECTION_NAME).count == 0:
        return []

    query_vector = encoder.encode(query).tolist()
    
    search_result = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    )
    
    return [hit.payload for hit in search_result.points]