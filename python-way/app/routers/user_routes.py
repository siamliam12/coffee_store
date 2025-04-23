from fastapi import APIRouter,status,Depends
from app.crud import user_controller
from app.schemas.userSchema import UserOutput,CreateUser
from app.db.database import engine,SessionLocal,Base
from sqlalchemy.orm import Session
from app.utils.password_manager import get_hashed_password
from app.models import user_model
router = APIRouter()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
@router.get("/users")
def get_users():
    return user_controller.get_users()

@router.get("/users/{user_id}")
def get_users(user_id: int):
    return user_controller.get_user_by_id(user_id)

@router.post("/signup",status_code=status.HTTP_201_CREATED,response_model = UserOutput)
def create_user(user:CreateUser,db:Session = Depends(get_db)):
    # Hash The Password
    hashed_pass = get_hashed_password(user.password)

    user.password = hashed_pass

    new_user = user_model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user