#5.	Write a manual evaluation: prepare 5 question–expected answer pairs about your document. Run each through the RAG pipeline, score each answer as Correct / Partially Correct / Wrong, and calculate a simple accuracy percentage.

import os
import fitz  
from typing import List
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from groq import Groq

load_dotenv()

# Initialize Clients
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
encoder = SentenceTransformer("all-MiniLM-L6-v2")
qdrant_client = QdrantClient(":memory:")
collection_name = "eval_knowledge_base"

def extract_text_from_pdf(pdf_path: str) -> str:
    print(f"Loading document: {pdf_path}...")
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def setup_complex_database(pdf_path: str):
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

    raw_text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(raw_text, chunk_size=100, overlap=20)
    
    points = []
    for i, chunk in enumerate(chunks):
        vector = encoder.encode(chunk).tolist()
        points.append(PointStruct(id=i, vector=vector, payload={"text": chunk}))
    
    qdrant_client.upsert(collection_name=collection_name, points=points)
    print("Database Seeded Successfully.\n")

def retrieve(query: str, top_k: int = 2):
    query_vector = encoder.encode(query).tolist()
    search_result = qdrant_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
    )
    return [hit.payload['text'] for hit in search_result.points]

def build_prompt(query: str, chunks: List[str]) -> str:
    context_str = "\n".join([f"[{i+1}] {chunk}" for i, chunk in enumerate(chunks)])
    return f"""Context Information:
{context_str}

Question: {query}

Instructions: Answer using ONLY the context above. If the answer is not clearly present in the context, say exactly: "I don't know."
"""

def ask_pipeline(query):

    chunks = retrieve(query, top_k=2)

    prompt = build_prompt(query, chunks)

    response = groq_client.chat.completions.create(
        messages=[{"role":"user","content":prompt}],
        model="llama-3.3-70b-versatile",
        temperature=0.0,
    )

    answer = response.choices[0].message.content

    return answer, chunks

def main():
    print("TASK 5: INTERACTIVE RAG EVALUATION")
    print("*" * 35 + "\n")
    
    pdf_filename = "company_policy.pdf"
    if not os.path.exists(pdf_filename):
        print(f"ERROR: {pdf_filename} not found.")
        return
        
    setup_complex_database(pdf_filename)
    
    test_cases = [
        {
            "id": 1,
            "type": "Exact Conditions",
            "query": "Under what exact conditions does an employee lose the intellectual property rights to a side project they made on their own time and personal hardware?",
            "expected": "If the project utilizes features from 'core-utils-v4' OR if it directly competes with active R&D pipeline projects."
        },
        {
            "id": 2,
            "type": "Multiple Constraints",
            "query": "Can an employee buy a $450 ergonomic chair using their stipend, and how long must they wait normally for hardware refreshes?",
            "expected": "Yes, but they need VP authorization because it exceeds $400. Normal wait time is 36 months."
        },
        {
            "id": 3,
            "type": "Specific Details",
            "query": "What are the two requirements for a subcontractor to receive a temporary access card to the primary server room vault?",
            "expected": "A fully executed NDA-Form-9B AND physical escort by a staff member with at least 24 months of tenure."
        },
        {
            "id": 4,
            "type": "Negative Edge Case",
            "query": "What is the disciplinary action required for a third infraction within the progressive discipline track?",
            "expected": "I don't know."
        },
        {
            "id": 5,
            "type": "Completely Absent Data",
            "query": "What is the policy regarding health insurance coverage extensions for family dependents during maternity leave?",
            "expected": "I don't know."
        }
    ]
    
    total_score = 0.0
    score_map = {"c": 1.0, "p": 0.5, "w": 0.0}

    for item in test_cases:
        print(f"Test #{item['id']} ({item['type']})")
        print(f"Question : {item['query']}")
        print(f"Expected : {item['expected']}")
        
        actual_answer, _ = ask_pipeline(item["query"])
        print(f"AI Answer: {actual_answer}\n")
        
        # Interactive Grading Loop
        while True:
            grade = input("Grade this answer [C = Correct, P = Partial, W = Wrong]: ").strip().lower()
            if grade in score_map:
                total_score += score_map[grade]
                print("\n")
                break
            print("Invalid input. Please type C, P, or W.")

    # Calculate and display final accuracy
    accuracy = (total_score / len(test_cases)) * 100
    
    print("*" * 35)
    print("EVALUATION COMPLETE")
    print("*" * 35)
    print(f"Total Points : {total_score} / {len(test_cases)}")
    print(f"Accuracy     : {accuracy:.1f}%")

if __name__ == "__main__":
    main()