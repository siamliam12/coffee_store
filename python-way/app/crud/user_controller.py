from app.utils.auth import get_hashed_password,verify_password,create_access_token
from fastapi import HTTPException
from app.models import user_model
from datetime import timedelta
from app.utils.auth import get_hashed_password

def get_users(db):
    allUsers = db.query(user_model.User).all()
    return {"Users": allUsers}

def get_user_by_id(user_id: int,db):
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    cards = db.query(user_model.IDCard).filter(user_model.IDCard.user_id == user_id).all()
    return {"User": {user},"All cards": cards}

def create_user(user: dict,db):
    try:
        existing_user = db.query(user_model.User).filter(user_model.User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        # Hash The Password
        hashed_pass = get_hashed_password(user.password)
        user.password = hashed_pass
        new_user = user_model.User(**user.dict())
        db.add(new_user)
        db.commit()
        
        return new_user
    except Exception as e:
        db.rollback()
        return {"message": f"Error creating user: {str(e)}"}

def login_user(form_data,db):
    user = db.query(user_model.User).filter(user_model.User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect Email or password")
    
    token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": token, "token_type": "bearer"}

def update_user(user_id: int,user: dict,db,current_user):
    try:
        # Check if the user is a manager
        if current_user.role != "manager":
            raise HTTPException(status_code=400, detail="You are not authorized to update user")
        existing_user = db.query(user_model.User).filter(user_model.User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        # Check if the user exists
        db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
        # If not, raise an HTTPException with a 404 status code
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        # Update the user details
        update_data = user.dict(exclude_unset=True)
        if "password" in update_data:
            # Hash the new password
            update_data["password"] = get_hashed_password(update_data["password"])

        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return {"User": db_user}
    except HTTPException as he:
        return he
    except Exception as e:
        return {"error": str(e)}
    
def delete_user(user_id: int,db,current_user):
    try:
        # Check if the user is a manager
        if current_user.role != "manager":
            raise HTTPException(status_code=400, detail="You are not authorized to delete user")
        # Check if the user exists
        db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
        # If not, raise an HTTPException with a 404 status code
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        # Delete the user
        db.delete(db_user)
        db.commit()
        return {"message": "User deleted successfully"}
    except HTTPException as he:
        return he
    except Exception as e:
        return {"error": str(e)}