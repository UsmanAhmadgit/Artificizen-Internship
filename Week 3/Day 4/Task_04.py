#4.	Write a build_prompt(query, chunks) function that inserts the retrieved chunks as numbered context items and appends: “Answer using only the context above. If the answer is not in the context, say: I don’t know.”

def build_prompt(query, chunks):
    """Formats retrieved chunks into a strict grounding prompt."""
    
    context_str = ""
    for i, chunk in enumerate(chunks):
        context_str += f"[{i+1}] {chunk.strip()}\n"
        
    prompt = f"""You are a precise assistant.

Context Information:
{context_str}

Question: {query}

Instructions: Answer using ONLY the context above. If the answer is not in the context, say exactly: "I don't know."
"""
    return prompt

def main():
    print("--- TASK 4: PROMPT AUGMENTATION ---")
    
    sample_chunks = [
        "The company was founded in 2015 by Jane Doe.",
        "Our headquarters are located in Austin, Texas."
    ]
    sample_query = "Where is the company located?"
    
    final_prompt = build_prompt(sample_query, sample_chunks)
    print("Generated Prompt:\n")
    print(final_prompt)

if __name__ == "__main__":
    main()