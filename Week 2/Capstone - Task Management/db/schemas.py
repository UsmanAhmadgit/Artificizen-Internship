from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from db.models import TaskStatus

# USER SCHEMAS 
class UserCreate(BaseModel):
    email: EmailStr = Field(description="Must be a valid email format")
    password: str = Field(
        min_length=8, 
        max_length=50, 
        description="Password must be between 8 and 50 characters"
    )

class UserRead(BaseModel):
    id: int
    email: EmailStr
    
    class Config:
        from_attributes = True

# TASK SCHEMAS
class TaskBase(BaseModel):
    title: str = Field(
        min_length=1, 
        max_length=100, 
        description="Task title cannot be empty and max 100 characters"
    )
    description: Optional[str] = Field(
        default=None, 
        max_length=1000, 
        description="Optional detailed description, max 1000 characters"
    )
    status: TaskStatus = Field(
        default=TaskStatus.pending,
        description="Task status: pending, in_progress, or done"
    )
    due_date: Optional[datetime] = Field(
        default=None,
        description="Optional deadline for the task"
    )

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    owner_id: int
    
    class Config:
        from_attributes = True