#1.	Expose your Day 4 RAG pipeline as POST /chat in FastAPI. The response body must include answer (string) and sources (list of chunk metadata dicts).

import os
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from groq import Groq

# 1. Environment & Client Setup
load_dotenv()

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
encoder = SentenceTransformer("all-MiniLM-L6-v2")
qdrant_client = QdrantClient(":memory:")
collection_name = "task1_knowledge_base"

# 2. FastAPI App Setup
app = FastAPI(title="Day 5 Task 1 - RAG API", version="1.0")

# 3. Request & Response Schemas (Pydantic Models)
class ChatRequest(BaseModel):
    query: str

class SourceItem(BaseModel):
    filename: str
    chunk_index: int
    text: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceItem]

# 4. Ingestion / Database Setup (Adapted from Day 4)
@app.on_event("startup")
def setup_database():
    """Sets up Qdrant collection on server startup and loads initial document chunks."""
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

    chunks = [
        "New York City is composed of five boroughs: Brooklyn, Queens, Manhattan, The Bronx, and Staten Island.",
        "The Statue of Liberty was a gift from France to the United States and was dedicated in 1886.",
        "Central Park, located in Manhattan, spans 843 acres and was established in 1857.",
        "The Empire State Building stands at 1,454 feet tall, including its antenna.",
    ]

    print("Embedding document chunks into Qdrant...")
    points = []
    for i, chunk in enumerate(chunks):
        vector = encoder.encode(chunk).tolist()
        # modification from DAY 4: Added 'filename' and 'chunk_index' to payload for citations
        payload = {
            "filename": "nyc_guide.pdf",
            "chunk_index": i,
            "text": chunk,
        }
        points.append(PointStruct(id=i, vector=vector, payload=payload))

    qdrant_client.upsert(collection_name=collection_name, points=points)
    print("Database initialized and populated successfully!")

def retrieve(query: str, top_k: int = 2):
    """Embeds query and fetches top-k chunks with complete payload metadata."""
    query_vector = encoder.encode(query).tolist()
    search_result = qdrant_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
    )
    return search_result.points

def build_prompt(query: str, hits) -> str:
    """Formats retrieved chunks into a strict grounding prompt."""
    context_str = "\n".join(
        [f"[{i+1}] {hit.payload['text']}" for i, hit in enumerate(hits)]
    )
    
    return f"""Context Information:
{context_str}

Question: {query}

Instructions: Answer using ONLY the context above. If the answer is not in the context, say exactly: "I don't know."
"""

# 7. POST /chat API Endpoint 
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # Step A: Retrieve relevant vector points (includes text + metadata)
    hits = retrieve(request.query, top_k=2)

    # Step B: Build grounded prompt & request generation from Groq
    prompt = build_prompt(request.query, hits)
    llm_response = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        temperature=0.0,
    )
    answer = llm_response.choices[0].message.content

    # Step C: Extract source citations from retrieved points
    sources = [
        SourceItem(
            filename=hit.payload["filename"],
            chunk_index=hit.payload["chunk_index"],
            text=hit.payload["text"],
        )
        for hit in hits
    ]

    return ChatResponse(answer=answer, sources=sources)