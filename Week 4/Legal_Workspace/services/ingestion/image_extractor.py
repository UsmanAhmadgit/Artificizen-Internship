from services.ingestion.ocr_utils import extract_text_from_image

def extract_image_chunks(file_bytes: bytes) -> list[str]:
    if not file_bytes or len(file_bytes) == 0:
        return []

    try:
        raw_text = extract_text_from_image(file_bytes)
        
        if not raw_text.strip():
            return []

        paragraphs = raw_text.split("\n")
        chunks = []
        current_chunk = []
        current_len = 0

        for para in paragraphs:
            clean_p = para.strip()
            if not clean_p:
                continue

            if len(clean_p) > 800:
                lines = clean_p.split(". ")
                for line in lines:
                    if current_len + len(line) > 800 and current_chunk:
                        chunks.append("\n".join(current_chunk))
                        last_item = current_chunk[-1]
                        current_chunk = [last_item, line]
                        current_len = len(last_item) + len(line)
                    else:
                        current_chunk.append(line)
                        current_len += len(line)
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

    except Exception as e:
        raise RuntimeError(f"Failed to process image file: {str(e)}")