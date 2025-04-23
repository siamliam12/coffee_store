from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class CreateUser(BaseModel):
    email : str
    password : str
    name: str

class UserLogin(BaseModel):
    email : str
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class DataToken(BaseModel):
    id:Optional[str] = None

class UserOutput(BaseModel):
    email: EmailStr 
    name: str
    id:int
    created_at:datetime = datetime.now()
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True