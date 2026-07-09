from pydantic import BaseModel, ConfigDict

# POST SCHEMAS
class PostRead(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    model_config = ConfigDict(from_attributes=True)

# USER SCHEMAS 
class UserCreate(BaseModel):
    name: str
    email: str

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)