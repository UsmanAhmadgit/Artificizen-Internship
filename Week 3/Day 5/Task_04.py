#4.	Add streaming using FastAPI’s StreamingResponse and stream=True on the Groq call. Verify tokens appear progressively with a curl command or the browser.

import os
import hashlib
import logging
from typing import List, Dict, Any, Generator
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from groq import Groq

# 1. Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("RAGStream")

# 2. Environment & Client Setup
load_dotenv()

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
encoder = SentenceTransformer("all-MiniLM-L6-v2")
qdrant_client = QdrantClient(":memory:")
collection_name = "task4_knowledge_base"

sessions_db: Dict[str, List[Dict[str, str]]] = {}
query_cache: Dict[str, Dict[str, Any]] = {}

# 4. FastAPI App Setup
app = FastAPI(title="Day 5 Task 4 - Streaming RAG API", version="1.0")

# 5. Request Schema
class ChatRequest(BaseModel):
    query: str
    session_id: str = Field(default="default_session", description="Session ID for chat history")

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

# 7. Helper: MD5 Query Hash
def get_query_hash(query: str) -> str:
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

# 9. Generator Function for Streaming Tokens
def generate_stream_response(query_str: str, session_id: str, query_hash: str) -> Generator[str, None, None]:
    """Yields LLM tokens one-by-one as they arrive from Groq, and updates memory/cache."""
    
    # Check Cache Hit
    if query_hash in query_cache:
        logger.info(f"[CACHE HIT] Key: {query_hash} | Query: '{query_str}'")
        cached_answer = query_cache[query_hash]["answer"]
        
        # Stream cached answer token by token
        for word in cached_answer.split():
            yield word + " "
            
        # Update Session History
        if session_id not in sessions_db:
            sessions_db[session_id] = []
        sessions_db[session_id].append({"role": "user", "content": query_str})
        sessions_db[session_id].append({"role": "assistant", "content": cached_answer})
        return

    # Cache Miss - Run RAG Retrieval
    logger.info(f"[CACHE MISS] Key: {query_hash} | Query: '{query_str}'")
    
    if session_id not in sessions_db:
        sessions_db[session_id] = []

    history = sessions_db[session_id]
    hits = retrieve(query_str, top_k=2)
    system_prompt = build_system_context(hits)

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history[-6:])
    messages.append({"role": "user", "content": query_str})

    # Call Groq with stream=True
    completion_stream = groq_client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile",
        temperature=0.0,
        stream=True,
    )

    full_response_acc = []

    for chunk in completion_stream:
        token = chunk.choices[0].delta.content or ""
        if token:
            full_response_acc.append(token)
            yield token  

    full_answer = "".join(full_response_acc)

    # Save to Session History
    history.append({"role": "user", "content": query_str})
    history.append({"role": "assistant", "content": full_answer})
    sessions_db[session_id] = history[-6:]

    # Save to Cache
    query_cache[query_hash] = {
        "answer": full_answer,
        "sources": [
            {
                "filename": hit.payload["filename"],
                "chunk_index": hit.payload["chunk_index"],
                "text": hit.payload["text"],
            }
            for hit in hits
        ],
    }

# 10. Streaming POST Endpoint
@app.post("/chat/stream")
def chat_stream_endpoint(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    query_str = request.query.strip()
    session_id = request.session_id.strip()
    query_hash = get_query_hash(query_str)

    return StreamingResponse(
        generate_stream_response(query_str, session_id, query_hash),
        media_type="text/plain",
    )