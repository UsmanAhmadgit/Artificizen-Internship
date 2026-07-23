import fitz  # PyMuPDF
from fastapi import UploadFile, HTTPException
from typing import List

def extract_text(file: UploadFile, content: bytes) -> str:
    """Extracts text from PDF or TXT files with strict validation."""
    
    # Edge Case: Empty file uploaded
    if not content:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    filename = file.filename.lower()
    extracted_text = ""

    if filename.endswith(".pdf"):
        try:
            doc = fitz.open(stream=content, filetype="pdf")
            for page in doc:
                extracted_text += page.get_text()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse PDF file: {str(e)}")
    
    elif filename.endswith(".txt"):
        try:
            extracted_text = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="TXT file must be UTF-8 encoded.")
    
    else:
        # Edge Case: Unsupported file format
        raise HTTPException(status_code=415, detail="Unsupported file format. Only .pdf and .txt are allowed.")

    # Edge Case: File was processed, but contained no readable text
    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in the document. Ensure it is not an image-only PDF.")

    return extracted_text

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> List[str]:
    """Splits raw text into overlapping chunks."""
    words = text.split()
    chunks = []
    
    # Edge Case: Text is shorter than the chunk size
    if len(words) <= chunk_size:
        return [" ".join(words)]

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        
    return chunks