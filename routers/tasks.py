from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
import logging

from database import get_db
from schemas import TaskCreate, TaskResponse, TaskStatusUpdate
from services import task_services
from auth.dependencies import get_current_user
from auth.roles import require_roles
from model import User

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    dependencies=[Depends(get_current_user)]
)

# Get all tasks with filtering
@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    """List all tasks (admin/manager only)"""
    return task_services.get_all_tasks(db, skip=skip, limit=limit, status=status)


# Create a task
@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new task"""
    return task_services.create_task(db, task, current_user)


# Get task by ID
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get task details by ID"""
    return task_services.get_task_by_id(db, task_id)


# Update task status
@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    task_update: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update task status"""
    return task_services.update_task_status(db, task_id, task_update, current_user)


# Delete task
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "manager"))
):
    """Delete task (admin/manager only)"""
    return task_services.delete_task(db, task_id)


# Get tasks assigned to user
@router.get("/user/{user_id}", response_model=list[TaskResponse])
def get_tasks_by_user(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get tasks assigned to a user"""
    # Authorization check
    if current_user.role == "member" and current_user.id != user_id:
        logger.warning(f"Unauthorized user access attempt by {current_user.id} to user {user_id} tasks")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own tasks"
        )

    return task_services.get_tasks_by_user(db, user_id, skip=skip, limit=limit)