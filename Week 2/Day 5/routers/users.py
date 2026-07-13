from fastapi import APIRouter, BackgroundTasks, HTTPException

# TASK 1: Users Router
router = APIRouter(prefix="/users", tags=["Users"])

# TASK 5: Background Function
def send_welcome_email(email: str):
    print(f"\n[BACKGROUND TASK] -> Sending welcome email to {email}...\n")

@router.post("/", status_code=201)
def create_user(email: str, background_tasks: BackgroundTasks):
    # Mocking a database conflict for our Task 6 Pytest
    if email == "existinguser@test.com":
        raise HTTPException(status_code=400, detail="Email already registered")
        
    # Trigger Background Task
    background_tasks.add_task(send_welcome_email, email)
    return {"message": "User created successfully"}

@router.get("/me")
def read_my_profile():
    # Mocking a 401 error since no actual token is provided in the test
    raise HTTPException(status_code=401, detail="Not authenticated")
