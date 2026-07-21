#1.	Write a chunk_text(text, chunk_size=500, overlap=50) function that splits a long string into overlapping chunks. Print the number of chunks produced from a 3,000-word document.

def chunk_text(text, chunk_size=500, overlap=50):
    """Splits a long string into overlapping chunks."""
    chunks = []
    step = chunk_size - overlap
    
    for i in range(0, len(text), step):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
        
        if i + chunk_size >= len(text):
            break
            
    return chunks

def main():
    print("--- TASK 1: TEXT CHUNKING ---")
    
    # Generated a dummy 3,000-word document 
    dummy_word = "apple "
    long_document = dummy_word * 3000 
    
    print(f"Document Length: {len(long_document)} characters ({len(long_document.split())} words)")
    
    # Chunk the text
    chunks = chunk_text(long_document, chunk_size=500, overlap=50)
    
    print(f"Chunk Size: 500 characters")
    print(f"Overlap: 50 characters")
    print(f"Total chunks produced: {len(chunks)}")

if __name__ == "__main__":
    main()