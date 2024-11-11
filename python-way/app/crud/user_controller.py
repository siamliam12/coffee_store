
def get_users():
    return {"message": "Get all users"}

def get_user_by_id(user_id: int):
    return {"message": f"Get user with id {user_id}"}

def create_user(user: dict):
    return {"message": f"Create user with data {user}"}