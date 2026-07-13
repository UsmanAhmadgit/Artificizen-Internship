from fastapi import APIRouter

# TASK 1: Auth Router
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/token")
def login():
    return {"access_token": "fake-jwt-token", "token_type": "bearer"}
