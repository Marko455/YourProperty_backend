from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class PropertyCreate(BaseModel):
    title: str
    description: str
    price: float
    city: str

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    city: Optional[str] = None

class PropertyOut(BaseModel):
    id: UUID
    title: str
    description: str
    price: float
    city: str
    owner_id: str
