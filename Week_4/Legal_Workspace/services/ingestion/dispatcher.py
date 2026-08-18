from services.ingestion.pdf_extractor import extract_pdf_chunks
from services.ingestion.docx_extractor import extract_docx_chunks
from services.ingestion.csv_extractor import extract_csv_chunks
from services.ingestion.pptx_extractor import extract_pptx_chunks
from services.ingestion.text_extractor import extract_text_chunks
from services.ingestion.image_extractor import extract_image_chunks
from services.ingestion.media_extractor import extract_media_chunks

EXTRACTOR_MAP = {
    "pdf": extract_pdf_chunks,
    "docx": extract_docx_chunks,
    "csv": extract_csv_chunks,
    "pptx": extract_pptx_chunks,
    "txt": extract_text_chunks,
    "md": extract_text_chunks,
    
    "png": extract_image_chunks,
    "jpg": extract_image_chunks,
    "jpeg": extract_image_chunks,
    "webp": extract_image_chunks,
    
    "mp3": extract_media_chunks,
    "wav": extract_media_chunks,
    "m4a": extract_media_chunks,
    "aac": extract_media_chunks,
    "flac": extract_media_chunks,
    
    "mp4": extract_media_chunks,
    "mkv": extract_media_chunks,
    "mov": extract_media_chunks,
    "avi": extract_media_chunks,
    "webm": extract_media_chunks,
}

def parse_file_to_chunks(file_bytes: bytes, file_extension: str) -> list[str]:
    if not file_bytes or len(file_bytes) == 0:
        return []

    ext = file_extension.lower().lstrip(".")
    extractor = EXTRACTOR_MAP.get(ext)

    if not extractor:
        raise ValueError(f"Unsupported file format: .{ext}")

    media_extensions = {"mp3", "wav", "m4a", "aac", "flac", "mp4", "mkv", "mov", "avi", "webm"}
    
    if ext in media_extensions:
        return extractor(file_bytes, filename=f"upload.{ext}")
    else:
        return extractor(file_bytes)