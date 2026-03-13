from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from model import Project, Task
from schemas import ProjectCreate
import logging

logger = logging.getLogger(__name__)


def create_project(db: Session, project: ProjectCreate):
    """Create a new project"""
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    logger.info(f"Project created: {db_project.id}")
    return db_project


def get_all_projects(db: Session, skip: int = 0, limit: int = 10):
    """Get all projects with pagination"""
    return db.query(Project).offset(skip).limit(limit).all()


def get_project_by_id(db: Session, project_id: int):
    """Get project by ID"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project


def update_project(db: Session, project_id: int, project_update: ProjectCreate):
    """Update existing project"""
    project = get_project_by_id(db, project_id)
    
    for field, value in project_update.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    logger.info(f"Project updated: {project_id}")
    return project


def delete_project(db: Session, project_id: int):
    """Delete project (only if no tasks exist)"""
    project = get_project_by_id(db, project_id)

    task_count = db.query(Task).filter(Task.project_id == project_id).count()
    if task_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete project with existing tasks"
        )

    db.delete(project)
    db.commit()
    logger.info(f"Project deleted: {project_id}")
    return {"message": "Project deleted successfully"}


def get_tasks_by_project(db: Session, project_id: int):
    """Get all tasks in a project"""
    project = get_project_by_id(db, project_id)
    return db.query(Task).filter(Task.project_id == project_id).all()


