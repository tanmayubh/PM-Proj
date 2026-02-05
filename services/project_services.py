from sqlalchemy.orm import Session
from fastapi import HTTPException

from model import Project, Task
from schemas import ProjectCreate

def create_project(db: Session, project: ProjectCreate):
    db_project = Project(**project.model_dump())

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project

def get_all_projects(db: Session):
    return db.query(Project).all()

def delete_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    task_count = db.query(Task).filter(Task.project_id == project_id).count()
    if task_count > 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete project with existing tasks"
        )

    db.delete(project)
    db.commit()

    return {"message": "Project deleted successfully"}


