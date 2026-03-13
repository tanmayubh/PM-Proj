from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session
import logging

from database import get_db
from services import user_services
from schemas import UserCreate, UserResponse
from auth.roles import require_roles
from auth.dependencies import get_current_user
from model import User

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


# Create a user (admin only)
@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    """Create new user (admin only)"""
    return user_services.create_user(db, user)


# List all users with pagination (admin/manager only)
@router.get("/", response_model=list[UserResponse])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    """List all users with pagination (admin/manager only)"""
    return user_services.get_all_users(db, skip=skip, limit=limit)


# Get user by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user details by ID"""
    user = user_services.get_user_by_id(db, user_id)
    # Members can only view their own profile
    if current_user.role == "member" and current_user.id != user_id:
        logger.warning(f"Unauthorized user access attempt by {current_user.id} to user {user_id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only view your own profile")
    return user


# Update user role (admin only)
@router.patch("/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    new_role: str = Query(..., description="New role: admin, manager, or member"),
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    """Update user role (admin only)"""
    return user_services.update_user_role(db, user_id, new_role)


# Deactivate user (admin only)
@router.patch("/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    """Deactivate user account (admin only)"""
    user_services.deactivate_user(db, user_id)
    return {"message": f"User {user_id} deactivated"}


# Reactivate user (admin only)
@router.patch("/{user_id}/activate")
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    """Reactivate user account (admin only)"""
    user_services.activate_user(db, user_id)
    return {"message": f"User {user_id} reactivated"}