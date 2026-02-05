from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from schemas import TaskCreate, TaskResponse, TaskStatusUpdate
from services import task_services

from auth.dependencies import get_current_user

from auth.roles import require_roles

from model import User

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    dependencies=[Depends(get_current_user)]
)

# get all tasks
@router.get("/", response_model=list[TaskResponse], response_model_exclude_none=True)
def list_tasks(db: Session = Depends(get_db), current_user=Depends(require_roles("admin", "manager"))):
     return task_services.get_all_tasks(db)

# create a task
@router.post("/", response_model=TaskResponse, response_model_exclude_none=True)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return task_services.create_task(db, task, current_user)
  
# update task status
@router.patch("/{task_id}", response_model=TaskResponse, response_model_exclude_none=True)
def update_task_status(task_id: int, task_update: TaskStatusUpdate, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    return task_services.update_task_status(db, task_id, task_update, current_user)

# get task by user
@router.get("/user/{user_id}", response_model=list[TaskResponse], response_model_exclude_none=True)
def get_tasks_by_user(user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    
    if current_user.role == "member" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return task_services.get_tasks_by_user(db, user_id)