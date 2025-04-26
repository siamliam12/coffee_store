from fastapi import APIRouter,status,Depends
from app.crud import user_controller
from app.schemas.userSchema import CreateUser,UserOutput
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import get_db
from app.dependencies import get_current_user

router = APIRouter(tags=["Admin API"])

#get all users
@router.get("/users")
def get_users(db:Session = Depends(get_db)):
    return user_controller.get_users(db)

#get user by id
@router.get("/users/{user_id}")
def get_users_by_id(user_id: int,db:Session = Depends(get_db)):
    return user_controller.get_user_by_id(user_id,db)

#create user by id
@router.post("/signup",status_code=status.HTTP_201_CREATED,response_model = UserOutput,tags=["Authentication"])
def create_user(user:CreateUser,db:Session = Depends(get_db)):
    return user_controller.create_user(user,db)

#login user
@router.post("/login",tags=["Authentication"])
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return user_controller.login_user(form_data,db)

#update user by id
@router.put("/update_user/{user_id}",tags=["Admin API"])
def update_user(
    user_id: int,
    user: CreateUser,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):
    return user_controller.update_user(user_id,user,db,current_user)

#delete user by id
@router.delete("/delete_user/{user_id}",tags=["Admin API"])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):
    return user_controller.delete_user(user_id,db,current_user)