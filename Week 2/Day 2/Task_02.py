#2.	Add a Field() constraint to email requiring it to match a basic email pattern, and age must be between 18 and 120.

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: int = Field(ge=18, le=120)

@app.post("/users")
def create_user(user: UserCreate):
    return user