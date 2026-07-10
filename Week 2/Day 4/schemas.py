from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator

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
    email: EmailStr
    password: str

    @field_validator('name')
    @classmethod
    def validate_name_length(cls, v:str):
        if len(v) < 1:
            raise ValueError("Name must be at least 1 character long")
        if len(v) > 50:
            raise ValueError("Name cannot exceed 50 characters")

    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v: str):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if len(v) > 50:
            raise ValueError("Password cannot exceed 50 characters")            
        return v

class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    role: str
    model_config = ConfigDict(from_attributes=True)