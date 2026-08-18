import io
import pandas as pd

def extract_csv_chunks(file_bytes: bytes) -> list[str]:
    if not file_bytes or len(file_bytes) == 0:
        return []

    df = None
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(io.BytesIO(file_bytes), encoding=encoding)
            break
        except Exception:
            continue

    if df is None:
        raise RuntimeError("Failed to parse CSV: file encoding not supported or binary corrupted")

    if df.empty:
        return []

    df = df.fillna("N/A")
    headers = [str(col).strip() for col in df.columns]

    rows_text = []
    for idx, row in df.iterrows():
        row_items = []
        for h in headers:
            val = str(row[h]).strip()
            if val and val != "N/A":
                row_items.append(f"{h}: {val}")
        
        if row_items:
            row_sentence = f"Row {idx + 1} -> " + " | ".join(row_items)
            rows_text.append(row_sentence)

    if not rows_text:
        return []

    chunks = []
    current_chunk = []
    current_len = 0

    for r in rows_text:
        if current_len + len(r) > 800 and current_chunk:
            chunks.append("\n".join(current_chunk))
            current_chunk = [r]
            current_len = len(r)
        else:
            current_chunk.append(r)
            current_len += len(r)

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks