#5.	Protect GET /users/me with the get_current_user dependency so only authenticated users can access it.

from fastapi import APIRouter, Depends
import schemas, models

from Task_04 import get_current_user

router = APIRouter(prefix="/users", tags=["Task 5 - Protected Routes"])

@router.get("/me", response_model=schemas.UserRead)
def read_my_profile(current_user: models.User = Depends(get_current_user)):
    
    return current_user