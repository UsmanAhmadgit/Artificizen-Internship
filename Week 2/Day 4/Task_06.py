#6.	Add a role field to your user model. Write a require_admin dependency that raises 403 if the current user is not an admin, and apply it to a DELETE /users/{id} route.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models

from database import get_db
from Task_04 import get_current_user

router = APIRouter(prefix="/users", tags=["Task 6 - Role-Based Access"])

def require_admin(current_user: models.User = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )
        
    return current_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_admin: models.User = Depends(require_admin)):
    
    user_to_delete = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    db.delete(user_to_delete)
    db.commit()
    
    return