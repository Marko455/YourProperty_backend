from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class PropertyBase(BaseModel):
    title: str
    description: str
    rooms: int
    bathrooms: int
    bedrooms: int
    parking_spots: int
    price: Decimal
    location: str
    type: str

class PropertyCreate(PropertyBase):
    owner_id: str

class PropertyUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    rooms: Optional[int]
    bathrooms: Optional[int]
    bedrooms: Optional[int]
    parking_spot: Optional[int]
    price: Optional[Decimal]
    location: Optional[str]
    type: Optional[str]

class Property(PropertyBase):
    property_id: str
    owner_id: str
