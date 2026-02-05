from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from services import user_services
from schemas import  UserCreate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

#Create a User
@router.post("/", response_model= UserResponse, response_model_exclude_none=True)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    return user_services.create_user(db, user)

#List all users
@router.get("/", response_model=list[UserResponse], response_model_exclude_none=True)
def list_users(db: Session = Depends(get_db)):
    return user_services.get_all_users(db)