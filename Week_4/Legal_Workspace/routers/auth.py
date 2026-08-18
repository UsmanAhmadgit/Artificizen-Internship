from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, EmailStr, Field
from datetime import timedelta
from services.embedder import delete_file_vectors
import os

from db.database import get_db
from db.models import User
from services.auth import verify_password, get_password_hash, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username must be between 3 and 50 characters")
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100, description="Password must be at least 6 characters long")

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pwd = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_pwd)
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email or username already registered"
        )
        
    return {"id": db_user.id, "username": db_user.username, "email": db_user.email}


@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
        
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")))
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer", "username": user.username}

@router.delete("/account", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_account(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user.id).first()
    
    if user:
        for room in user.rooms:
            for db_file in room.files:
                
                if os.path.exists(db_file.file_path):
                    os.remove(db_file.file_path)

                delete_file_vectors(db_file.id)

        db.delete(user)
        db.commit()
        
    return None