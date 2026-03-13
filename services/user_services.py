

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from model import User
from schemas import UserCreate
from auth.security import hash_password
import logging

logger = logging.getLogger(__name__)

VALID_ROLES = {"admin", "manager", "member"}


def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user in the database.
    Validates role and checks for existing username/email.
    Password is hashed with bcrypt.
    """
    # Check if username or email already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists"
        )

    if user.role not in VALID_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {', '.join(VALID_ROLES)}"
        )
    
    # Hash the password
    hashed = hash_password(user.password)

    # Create user object
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed,
        role=user.role,
        is_active=True
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"New user created: {user.username} with role {user.role}")
    return db_user


def get_all_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
    """Get all users with pagination"""
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int) -> User:
    """Get user by ID or raise 404"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


def get_user_by_username(db: Session, username: str) -> User:
    """Get user by username or None"""
    return db.query(User).filter(User.username == username).first()


def update_user_role(db: Session, user_id: int, new_role: str) -> User:
    """Update user's role (admin only operation)"""
    if new_role not in VALID_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {', '.join(VALID_ROLES)}"
        )
    
    user = get_user_by_id(db, user_id)
    user.role = new_role
    db.commit()
    db.refresh(user)
    logger.info(f"User {user_id} role updated to {new_role}")
    return user


def deactivate_user(db: Session, user_id: int) -> User:
    """Deactivate user account (soft delete)"""
    user = get_user_by_id(db, user_id)
    user.is_active = False
    db.commit()
    db.refresh(user)
    logger.warning(f"User {user_id} ({user.username}) deactivated")
    return user


def activate_user(db: Session, user_id: int) -> User:
    """Reactivate user account"""
    user = get_user_by_id(db, user_id)
    user.is_active = True
    db.commit()
    db.refresh(user)
    logger.info(f"User {user_id} ({user.username}) reactivated")
    return user
