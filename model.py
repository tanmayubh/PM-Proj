from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Boolean
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    tasks = relationship("Task", backref="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project id={self.id} name={self.name}>"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="todo")
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    priority = Column(Integer, default=3)
    due_date = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_to = relationship("User", backref="tasks")

    def __repr__(self):
        return f"<Task id={self.id} title={self.title}>"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"