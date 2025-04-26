from pydantic import BaseModel

from datetime import datetime

class CreateIDCard(BaseModel):
    # card_number :int
    user_id :int
    issue_date :datetime = datetime.now()
    expiration_date :str
    status : str  # e.g., 'active', 'inactive', 'lost'
    issue_location : str  # e.g., 'New York', 'Los Angeles'

class IDCardOutput(BaseModel):
    card_number: int
    issue_date: str
    id:int
    expiration_date :str
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True