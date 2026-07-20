from qdrant_client import QdrantClient, models  
from sentence_transformers import SentenceTransformer
import uuid

def embed_and_store(client: QdrantClient, collection_name: str, texts: list[str], metadata_list: list[dict]):
    
    # 1. Initialize the embedding model
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    
    print(f"Embedding {len(texts)} documents...")
    
    # 2. Batch encode all texts 
    vectors = encoder.encode(texts)
    
    # 3. Prepare the points for Qdrant
    points = []
    for vector, text, metadata in zip(vectors, texts, metadata_list):
        payload = {"text": text}
        payload.update(metadata)
        
        points.append(
            models.PointStruct(
                id=str(uuid.uuid4()), 
                vector=vector.tolist(),
                payload=payload
            )
        )
        
    # 4. Upsert into the database
    print(f"Upserting to collection '{collection_name}'...")
    client.upsert(
        collection_name=collection_name,
        points=points
    )
    print("Upload complete.\n")

def main():
    print("--- TASK 6: RAG UTILITY TESTING ---")
    
    # Setup test environment
    test_client = QdrantClient(":memory:")
    collection = "my_rag_data"
    
    test_client.create_collection(
        collection_name=collection,
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
    )
    
    # Test data
    texts_to_upload = [
        "Our refund policy lasts 30 days.",
        "You can contact support at help@company.com."
    ]
    
    metadata = [
        {"category": "policy", "department": "billing"},
        {"category": "contact", "department": "support"}
    ]
    
    # Run the utility function
    embed_and_store(
        client=test_client,
        collection_name=collection,
        texts=texts_to_upload,
        metadata_list=metadata
    )
    
    count_info = test_client.count(collection_name=collection)
    print(f"Success! Collection currently holds {count_info.count} vectors.")

if __name__ == "__main__":
    main()
