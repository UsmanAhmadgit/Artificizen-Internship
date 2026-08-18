from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from db.database import get_db
from db.models import ChatRoom, ChatMessage, User
from services.auth import get_current_user
from services.rag import generate_chat_response

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    query: str

class SourceItem(BaseModel):
    filename: str
    file_type: str
    chunk_index: int
    excerpt: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceItem]

@router.post("/{room_id}", response_model=ChatResponse)
def send_message(room_id: int, req: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
        
    if room.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this room")

    history = db.query(ChatMessage)\
        .filter(ChatMessage.room_id == room_id)\
        .order_by(ChatMessage.created_at.desc())\
        .limit(6)\
        .all()
    
    history.reverse()

    rag_result = generate_chat_response(req.query, room_id, history)

    user_msg = ChatMessage(
        room_id=room_id, 
        user_id=current_user.id, 
        role="user", 
        content=req.query
    )
    db.add(user_msg)

    assistant_msg = ChatMessage(
        room_id=room_id, 
        user_id=current_user.id, 
        role="assistant", 
        content=rag_result["answer"],
        sources=rag_result["sources"]
    )
    db.add(assistant_msg)
    
    db.commit()

    return ChatResponse(
        answer=rag_result["answer"],
        sources=rag_result["sources"]
    )

@router.get("/{room_id}/history")
def get_chat_history(room_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
        
    if room.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this history")

    messages = db.query(ChatMessage)\
        .filter(ChatMessage.room_id == room_id)\
        .order_by(ChatMessage.created_at.asc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return messages

@router.delete("/{room_id}/history")
def clear_chat_history(room_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
        
    if room.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the room owner can clear history")

    db.query(ChatMessage).filter(ChatMessage.room_id == room_id).delete()
    db.commit()
    
    return {"detail": "Chat history cleared successfully"}