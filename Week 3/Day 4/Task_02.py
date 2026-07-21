#2.	Load a plain-text or PDF file, chunk it, embed all chunks with sentence-transformers, and store them in Qdrant with source filename and chunk index as metadata.

import os
import pymupdf4llm
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from Task_01 import chunk_text

def main():
    print("--- TASK 2: EMBED AND STORE ---")
    
    filename = "company_policy.pdf"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        return

    print(f"Extracting text from {filename}...")
    # to_markdown extracts the text and keeps formatting like headers and lists intact
    text_data = pymupdf4llm.to_markdown(filename)
    
    chunks = chunk_text(text_data, chunk_size=200, overlap=50)
    print(f"Generated {len(chunks)} chunks from the PDF.")
    
    print("Initializing embedding model and Qdrant...")
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    client = QdrantClient(":memory:")
    collection_name = "pdf_chunks"
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    
    # 5. Embed and Store
    print("Embedding and storing in Qdrant...")
    points = []
    for i, chunk in enumerate(chunks):
        vector = encoder.encode(chunk).tolist()
        points.append(
            PointStruct(
                id=i,
                vector=vector,
                payload={"filename": filename, "chunk_index": i, "text": chunk}
            )
        )
        
    client.upsert(collection_name=collection_name, points=points)
    print("Upload complete. PDF data is now searchable in Qdrant!")

if __name__ == "__main__":
    main()