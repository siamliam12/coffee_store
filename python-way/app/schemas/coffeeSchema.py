from pydantic import BaseModel

class CoffeeCreate(BaseModel):
    name: str
    description: str
    introduced: str
    price: float
    # image will be uploaded separately via Form, not part of JSON schema
