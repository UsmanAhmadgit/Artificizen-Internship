def extract_text_chunks(file_bytes: bytes) -> list[str]:
    if not file_bytes or len(file_bytes) == 0:
        return []

    content = None
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            content = file_bytes.decode(encoding)
            break
        except UnicodeDecodeError:
            continue

    if content is None:
        content = file_bytes.decode('utf-8', errors='ignore')

    paragraphs = content.split("\n\n")
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