from groq import Groq
from typing import List, Dict, Generator
from app.config import settings

groq_client = Groq(api_key=settings.GROQ_API_KEY)
MODEL_NAME = "llama-3.3-70b-versatile"

def build_system_prompt(context_chunks: List[dict]) -> str:
    """Formats context chunks into a strict grounding prompt."""
    if not context_chunks:
        context_str = "No relevant document context found."
    else:
        context_str = "\n\n".join(
            [f"[{i+1}] (File: {chunk['filename']}, Chunk: {chunk['chunk_index']})\n{chunk['text']}" 
             for i, chunk in enumerate(context_chunks)]
        )

    return f"""You are a strict, precise document Q&A assistant.

Instructions:
1. Answer the user's question strictly using ONLY the retrieved context provided below.
2. If the answer is not clearly and directly present in the context below, say exactly: "I don't know."
3. Do NOT make assumptions, extrapolate, or use pre-existing external knowledge.

Retrieved Context:
{context_str}"""

def generate_answer(
    query: str, 
    context_chunks: List[dict], 
    history: List[Dict[str, str]]
) -> str:
    """Executes a non-streaming Groq call and returns the complete text answer."""
    system_prompt = build_system_prompt(context_chunks)
    
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": query})

    response = groq_client.chat.completions.create(
        messages=messages,
        model=MODEL_NAME,
        temperature=0.0
    )
    return response.choices[0].message.content

def generate_stream_tokens(
    query: str, 
    context_chunks: List[dict], 
    history: List[Dict[str, str]]
) -> Generator[str, None, None]:
    """Yields token strings in real time as they arrive from the Groq API."""
    system_prompt = build_system_prompt(context_chunks)
    
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": query})

    stream = groq_client.chat.completions.create(
        messages=messages,
        model=MODEL_NAME,
        temperature=0.0,
        stream=True
    )

    for chunk in stream:
        token = chunk.choices[0].delta.content or ""
        if token:
            yield token