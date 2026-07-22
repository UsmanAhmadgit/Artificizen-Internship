#3.	Implement a simple cache: hash the query string with hashlib.md5, store results in a dict, and return cached answers immediately on repeated queries. Log whether each request was a cache hit or miss.

import os
import hashlib
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from groq import Groq

# 1. Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("RAGCache")

# 2. Environment & Client Setup
load_dotenv()

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
encoder = SentenceTransformer("all-MiniLM-L6-v2")
qdrant_client = QdrantClient(":memory:")
collection_name = "task3_knowledge_base"


sessions_db: Dict[str, List[Dict[str, str]]] = {}
query_cache: Dict[str, Dict[str, Any]] = {}

# 4. FastAPI App Setup
app = FastAPI(title="Day 5 Task 3 - Caching RAG API", version="1.0")

# 5. Request & Response Schemas
class ChatRequest(BaseModel):
    query: str
    session_id: str = Field(default="default_session", description="Session ID for chat history")

class SourceItem(BaseModel):
    filename: str
    chunk_index: int
    text: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceItem]
    session_id: str
    cache_hit: bool

# 6. Populate Knowledge Base on Startup
@app.on_event("startup")
def setup_database():
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

    points = []
    for i, chunk in enumerate(chunks):
        vector = encoder.encode(chunk).tolist()
        payload = {
            "filename": "nyc_guide.pdf",
            "chunk_index": i,
            "text": chunk,
        }
        points.append(PointStruct(id=i, vector=vector, payload=payload))

    qdrant_client.upsert(collection_name=collection_name, points=points)
    logger.info("Database initialized and populated successfully!")

# 7. Helper: Hash Function
def get_query_hash(query: str) -> str:
    """Normalizes the string and computes its MD5 hexadecimal digest."""
    normalized_query = query.strip().lower()
    return hashlib.md5(normalized_query.encode("utf-8")).hexdigest()

# 8. RAG Helpers
def retrieve(query: str, top_k: int = 2):
    query_vector = encoder.encode(query).tolist()
    search_result = qdrant_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
    )
    return search_result.points

def build_system_context(hits) -> str:
    context_str = "\n".join(
        [f"[{i+1}] {hit.payload['text']}" for i, hit in enumerate(hits)]
    )
    return f"""You are a precise assistant. Answer using ONLY the context provided below. If the answer cannot be deduced from the context, say exactly "I don't know."

Retrieved Context:
{context_str}"""

# 9. POST /chat Endpoint with MD5 Caching
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    query_str = request.query.strip()
    session_id = request.session_id.strip()

    # Step A: Generate MD5 hash of query string
    query_hash = get_query_hash(query_str)

    # Step B: Check Cache Hit
    if query_hash in query_cache:
        logger.info(f"[CACHE HIT] Key: {query_hash} | Query: '{query_str}'")
        cached_data = query_cache[query_hash]
        
        # Optionally update session history on cache hit
        if session_id not in sessions_db:
            sessions_db[session_id] = []
        sessions_db[session_id].append({"role": "user", "content": query_str})
        sessions_db[session_id].append({"role": "assistant", "content": cached_data["answer"]})

        return ChatResponse(
            answer=cached_data["answer"],
            sources=[SourceItem(**s) for s in cached_data["sources"]],
            session_id=session_id,
            cache_hit=True,
        )

    # Step C: Cache Miss - Run full RAG pipeline
    logger.info(f"[CACHE MISS] Key: {query_hash} | Query: '{query_str}'")

    if session_id not in sessions_db:
        sessions_db[session_id] = []

    history = sessions_db[session_id]
    hits = retrieve(query_str, top_k=2)
    system_prompt = build_system_context(hits)

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history[-6:])
    messages.append({"role": "user", "content": query_str})

    llm_response = groq_client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile",
        temperature=0.0,
    )
    answer = llm_response.choices[0].message.content

    # Update session history
    history.append({"role": "user", "content": query_str})
    history.append({"role": "assistant", "content": answer})
    sessions_db[session_id] = history[-6:]

    sources = [
        {
            "filename": hit.payload["filename"],
            "chunk_index": hit.payload["chunk_index"],
            "text": hit.payload["text"],
        }
        for hit in hits
    ]

    # Step D: Store output in Cache Dictionary
    query_cache[query_hash] = {
        "answer": answer,
        "sources": sources,
    }

    return ChatResponse(
        answer=answer,
        sources=[SourceItem(**s) for s in sources],
        session_id=session_id,
        cache_hit=False,
    )