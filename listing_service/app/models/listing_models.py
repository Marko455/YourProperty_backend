from pydantic import BaseModel

class ListingCreate(BaseModel):
    title: str
    description: str
    price: float
    city: str
    property_type: str
