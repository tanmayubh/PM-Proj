from sqlalchemy.orm import Session
from fastapi import HTTPException

from model import Task, Project, User
from schemas import TaskCreate, TaskStatusUpdate

def create_task(db: Session, task: TaskCreate, current_user: User) -> Task:
    # Validate project
    project = db.query(Project).filter(Project.id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    #ASSIGNMENT LOGIC
    assigned_user_id = current_user.id

    # Validate user (if provided)
    if task.assigned_user_id:
        if current_user.role not in {"admin", "manager"}:
            raise HTTPException(
                status_code=403,
                detail="Only admin or manager can assign tasks"
            )
        user = db.query(User).filter(User.id == task.assigned_user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Assigned user not found")
        
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

    return db_task

#list all tasks
def get_all_tasks(db: Session):
    return db.query(Task).all()

def get_tasks_by_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return db.query(Task).filter(Task.project_id == project_id).all()

def get_tasks_by_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return db.query(Task).filter(Task.user_id == user_id).all()

def update_task_status(db: Session, task_id: int, task_update: TaskStatusUpdate, current_user: User):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if current_user.role == "member" and task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own tasks")

    task.status = task_update.status
    db.commit()
    db.refresh(task)

    return task





