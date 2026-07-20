#2.	Write a function semantic_search(query, documents) that embeds the query, embeds all documents, and returns the top-3 most similar documents with their cosine similarity scores.

import numpy as np
from sentence_transformers import SentenceTransformer

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def semantic_search(query: str, documents: list[str]) -> list[dict]:

    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 1. Embed everything
    query_vector = model.encode(query)
    doc_vectors = model.encode(documents)
    
    # 2. Compute similarity for each document against the query
    results = []
    for doc, doc_vec in zip(documents, doc_vectors):
        score = cosine_similarity(query_vector, doc_vec)
        results.append({"document": doc, "score": score})
        
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:3]

def main():
    print("--- TASK 2: SEMANTIC SEARCH FUNCTION ---")
    
    docs = [
        "To reset your password, click the link sent to your email.",
        "Our office hours are Monday through Friday, 9am to 5pm.",
        "If you forgot your login credentials, tap 'trouble logging in'.",
        "The company cafeteria serves lunch from noon to 2pm.",
        "Update your account billing information in the settings tab."
    ]
    
    user_query = "How do I fix my password issue?"
    print(f"Query: '{user_query}'\n")
    
    top_results = semantic_search(user_query, docs)
    
    for rank, res in enumerate(top_results, 1):
        print(f"Rank {rank} (Score: {res['score']:.4f}): {res['document']}")

if __name__ == "__main__":
    main()