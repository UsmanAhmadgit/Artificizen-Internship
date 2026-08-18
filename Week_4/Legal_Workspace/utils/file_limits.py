def get_max_file_size(filename: str) -> int:
    ext = filename.split(".")[-1].lower()
    
    if ext in {"txt", "md", "csv"}:
        return 5 * 1024 * 1024       
    elif ext in {"pdf", "docx", "pptx"}:
        return 20 * 1024 * 1024       
    elif ext in {"png", "jpg", "jpeg", "webp"}:
        return 10 * 1024 * 1024       
    elif ext in {"mp3", "wav", "m4a", "aac", "flac"}:
        return 30 * 1024 * 1024       
    elif ext in {"mp4", "mkv", "mov", "avi", "webm"}:
        return 200 * 1024 * 1024       
    
    return 10 * 1024 * 1024  