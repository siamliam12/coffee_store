from fastapi import APIRouter,status,Depends
from app.crud import id_card_controller
from app.schemas.idcardSchema import IDCardOutput,CreateIDCard
from sqlalchemy.orm import Session
from app.dependencies import get_current_user
from app.dependencies import get_db

router = APIRouter(tags=["Admin API"])

#get all users
@router.get("/idcards")
def get_Id_Card(db:Session = Depends(get_db)):
    return id_card_controller.get_IdCard(db)

#get user by id
@router.get("/idcards/{idcard_id}")
def get_Id_Card_byID(card_number: int,db:Session = Depends(get_db)):
    return id_card_controller.get_IdCard_by_id(card_number,db)

#create user by id
@router.post("/create_id_card",status_code=status.HTTP_201_CREATED,response_model = IDCardOutput)
def create_Id_Card(card:CreateIDCard,db:Session = Depends(get_db),current_user=Depends(get_current_user)):
    return id_card_controller.create_IdCard(card,db,current_user)