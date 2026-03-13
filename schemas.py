from pydantic import BaseModel, EmailStr
from typing import Literal, Optional
from datetime import date, datetime

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int
    assigned_user_id: Optional[int] = None
    status: Literal["todo", "in_progress", "done"] = "todo"
    priority: int = 3
    due_date: Optional[date] = None

class TaskStatusUpdate(BaseModel):
    status: Literal["todo", "in_progress", "done"]

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    user_id: Optional[int] = None
    status: Literal["todo", "in_progress", "done"]
    project_id: int
    priority: int
    due_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Literal["admin", "manager", "member"]

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    