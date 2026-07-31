from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from services.embedder import delete_file_vectors
import os

from db.database import get_db
from db.models import ChatRoom, User
from services.auth import get_current_user

router = APIRouter(prefix="/rooms", tags=["Rooms"])

class RoomCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Name must be between 3 and 100 characters")
    description: Optional[str] = Field(None, max_length=255, description="Description can be up to 255 characters long")

class RoomUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=255)

class RoomResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room: RoomCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_room = ChatRoom(name=room.name, description=room.description, owner_id=current_user.id)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.get("/", response_model=List[RoomResponse])
def get_rooms(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rooms = db.query(ChatRoom).filter(ChatRoom.owner_id == current_user.id).all()
    return rooms

@router.put("/{room_id}", response_model=RoomResponse)
def update_room(room_id: int, room_update: RoomUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_room = db.query(ChatRoom).filter(ChatRoom.id == room_id, ChatRoom.owner_id == current_user.id).first()
    
    if not db_room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found or unauthorized")
        
    if room_update.name is not None:
        db_room.name = room_update.name
    if room_update.description is not None:
        db_room.description = room_update.description
        
    db.commit()
    db.refresh(db_room)
    return db_room

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_room = db.query(ChatRoom).filter(ChatRoom.id == room_id, ChatRoom.owner_id == current_user.id).first()
    
    if not db_room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found or unauthorized")
        
    for db_file in db_room.files:
        
        if os.path.exists(db_file.file_path):
            os.remove(db_file.file_path)

        delete_file_vectors(db_file.id)
            
    db.delete(db_room)
    db.commit()
    
    return None