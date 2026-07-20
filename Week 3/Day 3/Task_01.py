#1.	Use sentence-transformers with all-MiniLM-L6-v2 to embed “A dog is chasing a ball” and five other sentences. Compute cosine similarity between all pairs using numpy and rank them from most to least similar.

import numpy as np
from sentence_transformers import SentenceTransformer
import itertools

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def main():
    print("--- TASK 1: PAIRWISE COSINE SIMILARITY ---")
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    sentences = [
        "A dog is chasing a ball.",
        "The puppy runs after the toy.",
        "A cat is sleeping on the couch.",
        "The quick brown fox jumps over the lazy dog.",
        "A man is throwing a frisbee in the park.",
        "Data science involves machine learning and statistics."
    ]
    
    print("Embedding sentences...")
    embeddings = model.encode(sentences)
    
    results = []
    
    # Generate all unique pairs of indices (e.g., 0 and 1, 0 and 2, 1 and so on..)
    for i, j in itertools.combinations(range(len(sentences)), 2):
        score = cosine_similarity(embeddings[i], embeddings[j])
        results.append({
            "pair": (sentences[i], sentences[j]),
            "score": score
        })
        
    results.sort(key=lambda x: x["score"], reverse=True)
    
    print("\nRanked Pairs by Semantic Similarity:")
    for rank, result in enumerate(results, 1):
        print(f"{rank}. Score: {result['score']:.4f}")
        print(f"   A: '{result['pair'][0]}'")
        print(f"   B: '{result['pair'][1]}'\n")

if __name__ == "__main__":
    main()