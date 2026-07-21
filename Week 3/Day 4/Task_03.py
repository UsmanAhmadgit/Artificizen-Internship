#3.	Write a retrieve(query, collection, top_k=3) function that embeds the query with sentence-transformers and returns the top-k chunks from Qdrant.

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

def retrieve(query, client, encoder, collection_name, top_k=3):
    """Embeds the query and retrieves the top-k chunks from Qdrant."""
    query_vector = encoder.encode(query).tolist()
    
    search_result = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k
    )
    
    retrieved_chunks = [hit.payload['text'] for hit in search_result.points]
    return retrieved_chunks

def main():
    print("--- TASK 3: RETRIEVAL UTILITY ---")
    
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    client = QdrantClient(":memory:")
    collection_name = "test_collection"
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    
    # A dummy document
    docs = [
        "Mars is often called the Red Planet due to iron oxide on its surface.", 
        "NASA's Perseverance rover is currently exploring the Jezero Crater on Mars.", 
        "Olympus Mons is the largest volcano in the solar system, located on Mars.", 
        "The Earth's moon influences the ocean tides.", 
        "Photosynthesis is the process by which plants make food.", 
        "Python is heavily used in Artificial Intelligence and Web Development." 
    ]
    
    points = [PointStruct(id=i, vector=encoder.encode(doc).tolist(), payload={"text": doc}) for i, doc in enumerate(docs)]
    client.upsert(collection_name=collection_name, points=points)
    
    # Test retrieval with top_k=3
    query = "Tell me about Mars."
    print(f"\nQuery: '{query}'")
    print()
    
    # Fetch top 3 results
    results = retrieve(query, client, encoder, collection_name, top_k=3)
    
    # Display the results
    for i, chunk in enumerate(results):
        print(f"Result {i+1}: {chunk}")

if __name__ == "__main__":
    main()