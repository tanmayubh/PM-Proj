

from sqlalchemy.orm import Session
from fastapi import HTTPException

from model import User
from schemas import UserCreate

from auth.security import hash_password

VALID_ROLES = {"admin", "manager", "member"}

def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user in the database.
    Raises 409 if username or email already exists.
    Password is hashed with bcrypt (truncated to 72 chars).
    """
    # Check if username or email already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)).first()
    
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists"
        )

    if user.role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    #hash the password 
    hashed = hash_password(user.password)

    #create user object
    db_user = User(
        username=user.username,
        email=user.email,

        hashed_password=hashed,

        role=user.role
    )

    # Save to DB
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db: Session) -> list[User]:
    """Return all users"""
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int) -> User:
    """Return user by ID or raise 404"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user_by_username(db: Session, username: str) -> User:
    """Return user by username or None"""
    return db.query(User).filter(User.username == username).first()
