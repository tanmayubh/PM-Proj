from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from model import Task, Project, User
from schemas import TaskCreate, TaskStatusUpdate
import logging

logger = logging.getLogger(__name__)


def create_task(db: Session, task: TaskCreate, current_user: User) -> Task:
    """Create a new task with role-based assignment validation"""
    # Validate project exists
    project = db.query(Project).filter(Project.id == task.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Default: assign to current user
    assigned_user_id = current_user.id

    # Override assignment if manager/admin provided a specific user
    if task.assigned_user_id:
        if current_user.role not in {"admin", "manager"}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admin or manager can assign tasks"
            )
        user = db.query(User).filter(User.id == task.assigned_user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assigned user not found"
            )
        assigned_user_id = task.assigned_user_id
    
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        project_id=task.project_id,
        priority=task.priority,
        due_date=task.due_date,
        user_id=assigned_user_id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    logger.info(f"Task created: {db_task.id}")
    return db_task


def get_all_tasks(db: Session, skip: int = 0, limit: int = 10, status: str = None):
    """Get all tasks with pagination and optional status filter"""
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    return query.offset(skip).limit(limit).all()


def get_task_by_id(db: Session, task_id: int):
    """Get task by ID"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


def get_tasks_by_project(db: Session, project_id: int):
    """Get all tasks in a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return db.query(Task).filter(Task.project_id == project_id).all()


def get_tasks_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    """Get tasks assigned to a user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()


def update_task_status(db: Session, task_id: int, task_update: TaskStatusUpdate, current_user: User):
    """Update task status with role-based authorization"""
    task = get_task_by_id(db, task_id)
    
    # Members can only update their own tasks
    if current_user.role == "member" and task.user_id != current_user.id:
        logger.warning(f"Unauthorized update attempt by user {current_user.id} on task {task_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own tasks"
        )

    task.status = task_update.status
    db.commit()
    db.refresh(task)
    logger.info(f"Task {task_id} status updated to {task.status}")
    return task


def delete_task(db: Session, task_id: int):
    """Delete a task"""
    task = get_task_by_id(db, task_id)
    db.delete(task)
    db.commit()
    logger.info(f"Task deleted: {task_id}")
    return {"message": "Task deleted successfully"}





