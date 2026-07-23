from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas import ChatRequest, ChatResponse, SourceCitation
from app.services.document_service import extract_text, chunk_text
from app.services.vector_service import ingest_chunks, retrieve_context
from app.services.cache_service import cache_service
from app.services.memory_service import memory_service
from app.services.llm_service import generate_answer, generate_stream_tokens

app = FastAPI(
    title="Capstone Document Q&A Chatbot API",
    version="1.0.0",
    description="Production-grade RAG service powered by FastAPI, Qdrant, SentenceTransformers, and Groq."
)

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """Accepts PDF/TXT file upload, extracts text, chunks it, and indexes in Qdrant."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename missing from upload.")
    
    content = await file.read()
    raw_text = extract_text(file, content)
    chunks = chunk_text(raw_text, chunk_size=400, overlap=50)
    
    indexed_count = ingest_chunks(file.filename, chunks)
    return {
        "status": "success",
        "filename": file.filename,
        "chunks_indexed": indexed_count,
        "message": f"Successfully ingested {indexed_count} chunks into Qdrant."
    }

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """Handles standard chat queries with caching, context retrieval, and session memory."""
    session_id = request.session_id
    query = request.query

    # 1. Check Query Cache
    cached_result = cache_service.get(session_id, query)
    if cached_result:
        answer, raw_sources = cached_result
        memory_service.add_turn(session_id, query, answer)
        return ChatResponse(
            answer=answer,
            sources=[SourceCitation(**s) for s in raw_sources]
        )

    # 2. Retrieve top-3 chunks from Qdrant
    hits = retrieve_context(query, top_k=3)

    # 3. Fetch Session History
    history = memory_service.get_history(session_id)

    # 4. Generate LLM Answer
    answer = generate_answer(query, hits, history)

    # 5. Format Sources
    sources = [
        {
            "filename": hit["filename"],
            "chunk_index": hit["chunk_index"],
            "text": hit["text"]
        }
        for hit in hits
    ]

    # 6. Update Cache and Session Memory
    cache_service.set(session_id, query, answer, sources)
    memory_service.add_turn(session_id, query, answer)

    return ChatResponse(
        answer=answer,
        sources=[SourceCitation(**s) for s in sources]
    )

@app.post("/chat/stream")
def chat_stream_endpoint(request: ChatRequest):
    """Streams response tokens progressively while managing cache and memory."""
    session_id = request.session_id
    query = request.query

    # Check Cache Hit
    cached_result = cache_service.get(session_id, query)
    if cached_result:
        cached_answer, _ = cached_result
        memory_service.add_turn(session_id, query, cached_answer)
        
        def stream_cached():
            for word in cached_answer.split():
                yield word + " "
        
        return StreamingResponse(stream_cached(), media_type="text/plain")

    # Cache Miss: Retrieve context & history
    hits = retrieve_context(query, top_k=3)
    history = memory_service.get_history(session_id)

    sources = [
        {
            "filename": hit["filename"],
            "chunk_index": hit["chunk_index"],
            "text": hit["text"]
        }
        for hit in hits
    ]

    def token_generator():
        accumulated_answer = []
        for token in generate_stream_tokens(query, hits, history):
            accumulated_answer.append(token)
            yield token
        
        full_answer = "".join(accumulated_answer)
        # Update Cache & History upon stream completion
        cache_service.set(session_id, query, full_answer, sources)
        memory_service.add_turn(session_id, query, full_answer)

    return StreamingResponse(token_generator(), media_type="text/plain")