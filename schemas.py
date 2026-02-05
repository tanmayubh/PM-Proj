from pydantic import BaseModel
from typing import Literal, Optional
from datetime import date

class ProjectCreate(BaseModel):
    name: str

class ProjectResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int
    user_id: int = None
    status: Literal["todo", "in_progress", "done"] = "todo"
    priority: int = 3
    due_date: Optional[date] = None

class TaskStatusUpdate(BaseModel):
    status: Literal["todo", "in_progress", "done"]

class TaskResponse(BaseModel):
    id: int
    title:str
    description: Optional[str]
    user_id: int = None
    status: Literal["todo", "in_progress", "done"]
    project_id: int
    priority: int
    due_date: date = None

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    role: Literal["admin", "manager", "member"] 
    
class UserResponse(BaseModel):
    id:int
    username:str
    email:str
    
    role: str

    class Config:
        from_attributes = True

    