from app.utils.auth import get_hashed_password
from app.models import user_model
from fastapi import HTTPException
import random

def get_IdCard(db):
    allIdCards = db.query(user_model.IDCard).all()
    return {"Id Cards": allIdCards}

def get_IdCard_by_id(card_number: int,db):
    idCard = db.query(user_model.IDCard).filter(user_model.IDCard.card_number == card_number).first()
    userId = idCard.user_id
    user = db.query(user_model.User).filter(user_model.User.id == userId).first()
    return {"Card":{idCard},"User":{user}}

def create_IdCard(card: dict,db,current_user):
    try:
        user = db.query(user_model.User).filter(user_model.User.id == card.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user and current_user.role == "manager":
            print(user.role)
            card_data = card.dict()
            card_number = random.randint(100000, 999999)
            card_data['card_number'] = card_number

            new_card = user_model.IDCard(**card_data)
            db.add(new_card)
            user.card_number = card_number
            db.commit()
            db.refresh(new_card)
            return new_card
        else:
            raise HTTPException(status_code=403, detail="Only managers can create ID cards")
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        return {"message": f"Error creating user: {str(e)}"}