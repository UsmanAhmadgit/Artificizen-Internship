#3.	Create a ChromaDB in-memory collection, add 10 short paragraphs from any topic, query it with a natural language question, and print the top-2 results.

import chromadb
from chromadb.utils import embedding_functions

def main():
    print("--- TASK 3: CHROMADB IN-MEMORY ---")
    
    client = chromadb.Client()
    
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    collection = client.create_collection(
        name="knowledge_base",
        embedding_function=ef
    )
    
    documents = [
        "Photosynthesis is how plants convert sunlight into energy.",
        "The Eiffel Tower is located in Paris, France.",
        "Water boils at 100 degrees Celsius at sea level.",
        "Python is a high-level programming language.",
        "The human heart has four chambers.",
        "Jupiter is the largest planet in our solar system.",
        "William Shakespeare wrote Romeo and Juliet.",
        "The Great Wall of China is visible from space.",
        "Albert Einstein developed the theory of relativity.",
        "The Pacific Ocean is the largest ocean on Earth."
    ]
    
    ids = [f"doc_{i}" for i in range(len(documents))]
    
    print("Adding documents to ChromaDB...")
    
    collection.upsert(
        documents=documents,
        ids=ids
    )
    
    query_text = "Who is the author of famous romantic tragedies?"
    print(f"\nQuerying: '{query_text}'")
    
    results = collection.query(
        query_texts=[query_text],
        n_results=2 
    )
    
    print("\nTop 2 Results:")
    for i, doc in enumerate(results['documents'][0]):
        distance = results['distances'][0][i]
        print(f"{i+1}. {doc} (Distance: {distance:.4f})")

if __name__ == "__main__":
    main()