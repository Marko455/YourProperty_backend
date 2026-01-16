from pydantic import BaseModel
from typing import Optional

class PropertyBase(BaseModel):
    title: str
    description: str
    price: float
    location: str
    type: str

class PropertyCreate(PropertyBase):
    owner_id: str

class PropertyUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    location: Optional[str]
    type: Optional[str]

class Property(PropertyBase):
    property_id: str
    owner_id: str
