#6.	Create both ItemCreate and ItemRead schemas for a product (name, price, in_stock). The read schema adds created_at. Use response_model to ensure created_at always appears in responses.

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class ItemCreate(BaseModel):
    name: str
    price: float
    in_stock: bool

class ItemRead(BaseModel):
    name: str
    price: float
    in_stock: bool
    created_at: datetime

@app.post("/items", response_model=ItemRead)
def create_item(item: ItemCreate):
    
    current_time = datetime.now()
    
    response_data = {
        **item.model_dump(),
        "created_at": current_time
    }
    
    return response_data