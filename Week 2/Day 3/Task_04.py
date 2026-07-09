#4.	Write a GET /users route that returns all users, with skip and limit query params applied to the DB query.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter(prefix="/users", tags=["Task 4 - Read All Users"])

@router.get("/", response_model=list[schemas.UserRead])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users