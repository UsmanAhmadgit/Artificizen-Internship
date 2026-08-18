import fitz
import pymupdf4llm
from services.ingestion.ocr_utils import extract_text_from_image

def extract_pdf_chunks(file_bytes: bytes) -> list[str]:
    if not file_bytes or len(file_bytes) == 0:
        return []

    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        if doc.is_encrypted:
            raise ValueError("PDF document is password protected or encrypted")
            
        md_text = pymupdf4llm.to_markdown(doc)

        for page in doc:
            for img in page.get_images():
                xref = img[0]
                base_image = doc.extract_image(xref)
                img_text = extract_text_from_image(base_image["image"])
                if img_text:
                    md_text += f"\n\n[OCR from PDF Image]:\n{img_text}\n\n"
        
        if not md_text or not md_text.strip():
            return []

        paragraphs = md_text.split("\n\n")
        chunks = []
        current_chunk = []
        current_len = 0

        for para in paragraphs:
            clean_p = para.strip()
            if not clean_p:
                continue

            if len(clean_p) > 800:
                lines = clean_p.split("\n")
                for line in lines:
                    clean_line = line.strip()
                    if not clean_line:
                        continue
                    if current_len + len(clean_line) > 800 and current_chunk:
                        chunks.append("\n".join(current_chunk))
                        last_item = current_chunk[-1]
                        current_chunk = [last_item, clean_line]
                        current_len = len(last_item) + len(clean_line)
                    else:
                        current_chunk.append(clean_line)
                        current_len += len(clean_line)
            else:
                if current_len + len(clean_p) > 800 and current_chunk:
                    chunks.append("\n\n".join(current_chunk))
                    last_item = current_chunk[-1]
                    current_chunk = [last_item, clean_p]
                    current_len = len(last_item) + len(clean_p)
                else:
                    current_chunk.append(clean_p)
                    current_len += len(clean_p)

        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        return chunks

    except ValueError as ve:
        raise ve
    except Exception as e:
        raise RuntimeError(f"Failed to parse PDF document: {str(e)}")