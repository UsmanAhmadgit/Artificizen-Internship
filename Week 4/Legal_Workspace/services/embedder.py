import uuid
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

qdrant_client = QdrantClient(":memory:") 
COLLECTION_NAME = "legal_documents"

embedder = SentenceTransformer("all-MiniLM-L6-v2")

VECTOR_SIZE = embedder.get_embedding_dimension()

try:
    qdrant_client.get_collection(COLLECTION_NAME)
except Exception:
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )

def embed_and_store(chunks: list[str], metadata: dict) -> int:
    if not chunks:
        return 0
        
    embeddings = embedder.encode(chunks)
    
    points = []
    for idx, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
        point_id = str(uuid.uuid4())
        
        payload = metadata.copy()
        payload["chunk_index"] = idx
        payload["text"] = chunk_text  
        
        points.append(
            PointStruct(
                id=point_id,
                vector=embedding.tolist(),
                payload=payload
            )
        )
        
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    
    return len(points)