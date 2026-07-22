#2.	Add conversation history: store the last 6 turns in memory per session and pass them as previous messages to Groq so follow-up questions work correctly.

import os
from typing import List, Dict
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from groq import Groq

# 1. Environment & Client Setup
load_dotenv()

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
encoder = SentenceTransformer("all-MiniLM-L6-v2")
qdrant_client = QdrantClient(":memory:")
collection_name = "task2_knowledge_base"

# 2. In-Memory Session Store for Conversation History
sessions_db: Dict[str, List[Dict[str, str]]] = {}

# 3. FastAPI App Setup
app = FastAPI(title="Day 5 Task 2 - Multi-Turn RAG API", version="1.0")

# 4. Request & Response Schemas
class ChatRequest(BaseModel):
    query: str
    session_id: str = Field(default="default_session", description="Unique session ID for conversation memory")

class SourceItem(BaseModel):
    filename: str
    chunk_index: int
    text: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceItem]
    session_id: str
    history_length: int

# 5. Populate Knowledge Base on Startup
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
    print("Database initialized and populated successfully!")

def retrieve(query: str, top_k: int = 2):
    query_vector = encoder.encode(query).tolist()
    search_result = qdrant_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
    )
    return search_result.points

def build_system_context(hits) -> str:
    """Builds a system prompt containing the retrieved RAG context."""
    context_str = "\n".join(
        [f"[{i+1}] {hit.payload['text']}" for i, hit in enumerate(hits)]
    )
    return f"""You are a precise assistant. Answer using ONLY the context provided below. If the answer cannot be deduced from the context, say exactly "I don't know."

Retrieved Context:
{context_str}"""

# 7. POST /chat Endpoint with Session History Management
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    session_id = request.session_id.strip()

    if session_id not in sessions_db:
        sessions_db[session_id] = []

    history = sessions_db[session_id]

    hits = retrieve(request.query, top_k=2)
    system_prompt = build_system_context(hits)

    trimmed_history = history[-6:]  

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(trimmed_history)
    messages.append({"role": "user", "content": request.query})

    llm_response = groq_client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile",
        temperature=0.0,
    )
    answer = llm_response.choices[0].message.content

    history.append({"role": "user", "content": request.query})
    history.append({"role": "assistant", "content": answer})

    sessions_db[session_id] = history[-6:]

    sources = [
        SourceItem(
            filename=hit.payload["filename"],
            chunk_index=hit.payload["chunk_index"],
            text=hit.payload["text"],
        )
        for hit in hits
    ]

    return ChatResponse(
        answer=answer,
        sources=sources,
        session_id=session_id,
        history_length=len(sessions_db[session_id]),
    )