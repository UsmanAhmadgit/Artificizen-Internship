#2.	Create a POST /auth/register route that accepts username + password, hashes the password, and saves the user.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

from Task_01 import hash_password

router = APIRouter(prefix="/auth", tags=["Task 2 - Authentication"])

@router.post("/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
        
    scrambled_password = hash_password(user.password)
    
    db_user = models.User(
        name=user.name, 
        email=user.email, 
        hashed_password=scrambled_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user