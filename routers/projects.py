from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import logging

from database import get_db
from services import project_services
from schemas import ProjectCreate, ProjectResponse, TaskResponse
from auth.roles import require_roles
from auth.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

# Get all projects with pagination
@router.get("/", response_model=list[ProjectResponse])
def list_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all projects with pagination"""
    return project_services.get_all_projects(db, skip=skip, limit=limit)


# Create a project
@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    """Create new project (admin/manager only)"""
    return project_services.create_project(db, project)


# Get project by ID
@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get project details by ID"""
    return project_services.get_project_by_id(db, project_id)


# Update project
@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_update: ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    """Update project (admin/manager only)"""
    return project_services.update_project(db, project_id, project_update)


# Delete a project safely
@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    """Delete project (admin only)"""
    return project_services.delete_project(db, project_id)


# Get tasks by project
@router.get("/{project_id}/tasks", response_model=list[TaskResponse])
def get_tasks_by_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get all tasks in a project"""
    return project_services.get_tasks_by_project(db, project_id)
