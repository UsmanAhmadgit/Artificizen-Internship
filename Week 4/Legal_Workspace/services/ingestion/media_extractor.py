import os
import tempfile
from groq import Groq

client = Groq()

def extract_media_chunks(file_bytes: bytes, filename: str = "media.mp3") -> list[str]:

    if not file_bytes or len(file_bytes) == 0:
        return []

    ext = os.path.splitext(filename)[1].lower()
    if not ext:
        ext = ".mp3"

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
            tmp_file.write(file_bytes)
            tmp_path = tmp_file.name

        with open(tmp_path, "rb") as file_obj:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(tmp_path), file_obj.read()),
                model="whisper-large-v3",
                response_format="verbose_json",
                temperature=0.0
            )

        segments = getattr(transcription, "segments", [])
        elements = []

        if segments:
            for seg in segments:
                start_sec = int(seg.get("start", 0))
                end_sec = int(seg.get("end", 0))
                
                start_fmt = f"{start_sec // 60:02d}:{start_sec % 60:02d}"
                end_fmt = f"{end_sec // 60:02d}:{end_sec % 60:02d}"
                
                text = seg.get("text", "").strip()
                if text:
                    elements.append(f"[{start_fmt} - {end_fmt}] {text}")
        else:
            full_text = getattr(transcription, "text", "").strip()
            if full_text:
                elements = [p.strip() for p in full_text.split(". ") if p.strip()]

        if not elements:
            return []

        chunks = []
        current_chunk = []
        current_len = 0

        for item in elements:
            if current_len + len(item) > 800 and current_chunk:
                chunks.append("\n".join(current_chunk))
                
                last_item = current_chunk[-1]
                current_chunk = [last_item, item]
                current_len = len(last_item) + len(item)
            else:
                current_chunk.append(item)
                current_len += len(item)

        if current_chunk:
            chunks.append("\n".join(current_chunk))

        return chunks

    except Exception as e:
        raise RuntimeError(f"Failed to transcribe media file: {str(e)}")

    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass