#5.	Wire everything together: retrieve() → build_prompt() → ask() (using Groq). Ask three questions — two with answers in the document and one without. Verify the model says “I don’t know” for the third.

import os
from dotenv import load_dotenv 
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from groq import Groq

load_dotenv()

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
encoder = SentenceTransformer('all-MiniLM-L6-v2')
qdrant_client = QdrantClient(":memory:")
collection_name = "rag_knowledge_base"

def setup_database():
    """Sets up Qdrant and uploads a dummy document."""
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    
    chunks = [
        "New York City is composed of five boroughs: Brooklyn, Queens, Manhattan, The Bronx, and Staten Island.",
        "The Statue of Liberty was a gift from France to the United States and was dedicated in 1886.",
        "Central Park, located in Manhattan, spans 843 acres and was established in 1857.",
        "The Empire State Building stands at 1,454 feet tall, including its antenna."
    ]
    
    print("Embedding document chunks into Qdrant...")
    points = [
        PointStruct(id=i, vector=encoder.encode(chunk).tolist(), payload={"text": chunk}) 
        for i, chunk in enumerate(chunks)
    ]
    qdrant_client.upsert(collection_name=collection_name, points=points)

def retrieve(query, top_k=2):
    """Embeds the query and fetches the best chunks."""
    query_vector = encoder.encode(query).tolist()
    search_result = qdrant_client.query_points(
        collection_name=collection_name, 
        query=query_vector, 
        limit=top_k
    )
    return [hit.payload['text'] for hit in search_result.points]

def build_prompt(query, chunks):
    """Constructs the grounded prompt for the LLM."""
    context_str = "\n".join([f"[{i+1}] {chunk}" for i, chunk in enumerate(chunks)])
    
    prompt = f"""Context Information:
{context_str}

Question: {query}

Instructions: Answer using ONLY the context above. If the answer is not in the context, say exactly: "I don't know."
"""
    return prompt

def ask(query):
    retrieved_chunks = retrieve(query)
    final_prompt = build_prompt(query, retrieved_chunks)
    
    response = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": final_prompt}],
        model="llama-3.3-70b-versatile",
        temperature=0.0 
    )
    
    return response.choices[0].message.content

def main():
    print("--- TASK 5: FULL RAG PIPELINE ---\n")
    setup_database()
    
    questions = [
        "How many boroughs make up New York City?",           
        "When was Central Park established?",                 
        "What is the total population of New York City?",    
        "Who is the current mayor of New York City?"           
    ]
    
    for i, q in enumerate(questions):
        print(f"\nQuestion {i+1}: {q}")
        answer = ask(q)
        print(f"Answer:   {answer}")

if __name__ == "__main__":
    main()