from fastapi import APIRouter, UploadFile, File, Form, Depends
from app.crud import coffee_controller
# from app.schemas.idcardSchema import 
from sqlalchemy.orm import Session
from app.dependencies import get_current_user
from app.dependencies import get_db

router = APIRouter(tags=["Admin API"])

class CreateCoffee:
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    image: UploadFile = File(...)

#get all coffee cards
@router.get("/",tags=["Customer API","Coffee API"])
def get_coffee(db:Session = Depends(get_db)):
    return coffee_controller.get_coffee(db)

#get coffee by id
@router.get("/{coffee_id}",tags=["Coffee API"])
def get_coffee_byID(coffee_id: int,db:Session = Depends(get_db)):
    return coffee_controller.get_coffee_by_id(coffee_id,db)

#create coffee by id
@router.post("/create_coffee",tags=["Coffee API"])
def create_coffee(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    image: UploadFile = File(...)
    ,db:Session = Depends(get_db),current_user=Depends(get_current_user)):
    return coffee_controller.create_coffee(name,description,price,image,db,current_user)

#update coffee by id
@router.put("/update_coffee/{coffee_id}",tags=["Coffee API"])
def update_coffee(
    coffee_id: int,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    image: UploadFile = File(...),
    db:Session = Depends(get_db),current_user=Depends(get_current_user)):
    return coffee_controller.update_coffee(coffee_id,name,description,price,image,db,current_user)

#delete coffee by id
@router.delete("/delete_coffee/{coffee_id}",tags=["Coffee API"])
def delete_coffee(coffee_id: int,db:Session = Depends(get_db),current_user=Depends(get_current_user)):
    return coffee_controller.delete_coffee(coffee_id,db,current_user)