import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import ChatRoom, UploadedFile, User
from services.auth import get_current_user  
from services.embedder import embed_and_store
from services.ingestion import parse_file_to_chunks

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/{room_id}")
async def upload_file(
    room_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    room = db.query(ChatRoom).filter(
        ChatRoom.id == room_id, 
        ChatRoom.owner_id == current_user.id
    ).first()
    
    if not room:
        raise HTTPException(status_code=404, detail="Room not found or unauthorized access")

    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{room_id}_{file.filename}"
    file_bytes = await file.read()
    
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    ext = file.filename.split('.')[-1].lower()
    db_file = UploadedFile(
        room_id=room_id,
        filename=file.filename,
        file_type=ext,
        file_path=file_path,
        status="processing"
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    try:
        chunks = parse_file_to_chunks(file_bytes, ext)

        if not chunks:
            raise ValueError("No extractable text content found in file")

        metadata = {
            "room_id": room_id,
            "file_id": db_file.id,
            "filename": db_file.filename,
            "file_type": db_file.file_type
        }
        chunks_created = embed_and_store(chunks, metadata)
        
        db_file.status = "ready"
        db.commit()
        db.refresh(db_file)
        
        return {
            "file_id": db_file.id, 
            "filename": db_file.filename,
            "chunks_created": chunks_created, 
            "status": db_file.status
        }
        
    except Exception as e:
        db_file.status = "failed"
        db_file.error_message = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")