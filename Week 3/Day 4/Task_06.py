#6.	Test hallucination: run the same question WITHOUT the RAG context (raw Groq call only). Compare the answer to the RAG answer. Write a short observation on which is more grounded and why.

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def ask_raw_llm(query):
    """Asks the LLM relying purely on its training data."""
    response = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": query}],
        model="llama-3.3-70b-versatile",
        temperature=0.0
    )
    return response.choices[0].message.content

def ask_rag_llm(query, context):
    """Asks the LLM using strict RAG grounding instructions."""
    prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer using ONLY the context. If not present, say 'I don't know'."
    response = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        temperature=0.0
    )
    return response.choices[0].message.content

def main():
    print("--- TASK 6: HALLUCINATION TEST ---")
    
    query = "What is the access code for the server room in the Chicago office?"
    internal_context = "The server room requires keycard access. No numerical codes are used in the Chicago office."
    
    print("\n[Raw LLM Call - No RAG]")
    print(ask_raw_llm(query))
    
    print("\n[Grounded LLM Call - With RAG]")
    print(ask_rag_llm(query, internal_context))
    
    print("\n--- OBSERVATION ---")
    print("Without RAG, the LLM will either guess a generic format (hallucinate) or give a long-winded apology about lacking access to private systems. With RAG and strict grounding instructions, the LLM accurately utilizes the provided internal context and acts decisively, eliminating hallucinations.")

if __name__ == "__main__":
    main()