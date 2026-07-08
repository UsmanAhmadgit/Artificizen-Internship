#4.	Create a nested model: Address with city and country, and embed it in a UserCreate model.

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Address(BaseModel):
    city: str
    country: str

class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    address: Address 

@app.post("/users")
def create_user(user: UserCreate):
    return user