from fastapi import APIRouter
from app.crud import user_controller

router = APIRouter()

@router.get("/users")
def get_users():
    return user_controller.get_users()

@router.get("/users/{user_id}")
def get_users(user_id: int):
    return user_controller.get_user_by_id(user_id)

@router.post("/users")
def create_user():
    return user_controller.create_user()