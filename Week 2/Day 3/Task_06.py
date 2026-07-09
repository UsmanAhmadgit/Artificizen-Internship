#6.	Add a Post model with a ForeignKey to User. Write a route GET /users/{user_id}/posts that returns all posts for that user.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter(prefix="/users", tags=["Task 6 - Read User Posts"])

@router.get("/{user_id}/posts", response_model=list[schemas.PostRead])
def read_user_posts(user_id: int, db: Session = Depends(get_db)):
    # First verify the user exists
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Fetch all posts where owner_id matches
    posts = db.query(models.Post).filter(models.Post.owner_id == user_id).all()
    return posts