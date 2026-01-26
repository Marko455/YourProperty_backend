from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class PropertyBase(BaseModel):
    title: str
    description: str
    price: Decimal
    location: str
    type: str

class PropertyCreate(PropertyBase):
    owner_id: str

class PropertyUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[Decimal]
    location: Optional[str]
    type: Optional[str]

class Property(PropertyBase):
    property_id: str
    owner_id: str
