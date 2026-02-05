from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from services import project_services
from schemas import ProjectCreate, ProjectResponse, TaskResponse

from auth.roles import require_roles

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

# Get all projects
@router.get("/", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return project_services.get_all_projects(db)


# Create a project
@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db), current_user=Depends(require_roles("admin", "manager"))):
    return project_services.create_project(db, project)


# Delete a project safely
@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_user=Depends(require_roles("admin"))):
    return project_services.delete_project(db, project_id)

# Get tasks by project
@router.get("/{project_id}/tasks", response_model=list[TaskResponse])
def get_tasks_by_project(project_id: int, db: Session = Depends(get_db)):
    return project_services.get_tasks_by_project(db, project_id)
