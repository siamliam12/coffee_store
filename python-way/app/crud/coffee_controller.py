import shutil
from app.models.coffee_model import Coffee
from fastapi import HTTPException

def get_coffee(db):
    allCoffee = db.query(Coffee).all()
    return {"Coffee": allCoffee}

def get_coffee_by_id(coffee_id,db):
    coffee = db.query(Coffee).filter(Coffee.id == coffee_id).first()
    return {"Coffee": coffee}

def create_coffee(name,description,price,image,db,current_user):
    if current_user.role != "manager":
        raise HTTPException(status_code=400, detail="You are not authorized to create coffee")
    image_path = f"images/{image.filename}"
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    try:
        new_coffee = Coffee(
        name=name,
        description=description,
        price=price,
        image_url=image_path  # just the path
        )
        db.add(new_coffee)
        db.commit()
        db.refresh(new_coffee)

        return new_coffee
    except HTTPException as he:
        return he
    except Exception as e:
        return {"error": str(e)}

def update_coffee(coffee_id,name,description,price,image,db,current_user):
    # Check if the user is a manager
    if current_user.role != "manager":
        raise HTTPException(status_code=400, detail="You are not authorized to update coffee")
    # Check if the coffee exists
    coffee = db.query(Coffee).filter(Coffee.id == coffee_id).first()
    # If not, raise an HTTPException with a 404 status code
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")
    # Update the coffee details
    # If an image is provided, save it and update the image_url
    if image:
        image_path = f"images/{image.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        coffee.image_url = image_path  # just the path
    coffee.name = name
    coffee.description = description
    coffee.price = price
    db.commit()
    db.refresh(coffee)
    return {"Coffee": coffee}
    
def delete_coffee(coffee_id,db,current_user):
    # Check if the user is a manager
    if current_user.role != "manager":
        raise HTTPException(status_code=400, detail="You are not authorized to delete coffee")
    # Check if the coffee exists
    coffee = db.query(Coffee).filter(Coffee.id == coffee_id).first()
    # If not, raise an HTTPException with a 404 status code
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")
    db.delete(coffee)
    db.commit()
    return {"message": "Coffee deleted successfully"}