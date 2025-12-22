from pydantic import BaseModel
from typing import List, Optional

class UserProfile(BaseModel):
    name: str
    phone: Optional[str]
    role: str = "user"

class FavoritesUpdate(BaseModel):
    listing_id: str
