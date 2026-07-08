#5.	Add a @field_validator to reject any name that contains numbers.

from fastapi import FastAPI
from pydantic import BaseModel, field_validator

app = FastAPI()

class UserCreate(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def reject_numbers_in_name(cls, value: str):
        if any(char.isdigit() for char in value):
            raise ValueError("Name cannot contain numeric characters.")
        
        return value

@app.post("/users")
def create_user(user: UserCreate):
    return user