#3.	Create a UserRead model that adds an id: int field. Use response_model=UserRead on the route so the response always includes an id.

from fastapi import FastAPI
from pydantic import BaseModel, Field
import random

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: int = Field(ge=18, le=120)

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    age: int

@app.post("/users", response_model=UserRead)
def create_user(user: UserCreate):
    
    fake_db_id = random.randint(1000, 9999)
    
    response_data = {
        "id": fake_db_id,
        **user.model_dump() 
    }
    
    return response_data