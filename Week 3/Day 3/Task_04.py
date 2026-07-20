#4.	Repeat the previous exercise using Qdrant (QdrantClient(':memory:')). Add payloads with a source field and filter results to only return documents where source == 'manual'.

from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

def main():
    print("--- TASK 4: QDRANT WITH METADATA FILTERING ---")
    
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    client = QdrantClient(":memory:")
    
    collection_name = "support_docs"
    
    # 2. Create collection (all-MiniLM-L6-v2 outputs 384-dimensional vectors)
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=384, 
            distance=models.Distance.COSINE
        )
    )
    
    documents = [
        ("Press the red button to shut down the machine.", "manual"),
        ("The CEO announced a new product today.", "news"),
        ("To replace the battery, unscrew the back panel.", "manual"),
        ("Company stock rose by 5 percent this quarter.", "news"),
        ("Press the green button to start the machine.", "manual"),
        ("The new software update improves performance.", "news")
    ]
    
    print("Embedding and uploading to Qdrant...")
    points = []
    for i, (text, source) in enumerate(documents):
        vector = encoder.encode(text).tolist() 
        points.append(
            models.PointStruct(
                id=i,
                vector=vector,
                payload={"text": text, "source": source}
            )
        )
        
    client.upsert(collection_name=collection_name, points=points)
    
    query_text = "How do I turn off the equipment?"
    query_vector = encoder.encode(query_text).tolist()
    
    print(f"\nQuery: '{query_text}'")
    print("Filter: source == 'manual'\n")
    
    search_result = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="source",
                    match=models.MatchValue(value="manual")
                )
            ]
        ),
        limit=2
    )
    
    for hit in search_result.points:
        print(f"Score: {hit.score:.4f} | Source: {hit.payload['source']} | Text: {hit.payload['text']}")

if __name__ == "__main__":
    main()