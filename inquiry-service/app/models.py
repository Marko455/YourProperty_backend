from pydantic import BaseModel
from typing import Optional

class InquiryCreate(BaseModel):
    property_id: str
    message: str

class InquiryUpdate(BaseModel):
    status: str

class InquiryResponse(BaseModel):
    inquiry_id: str
    property_id: str
    buyer_id: str
    message: str
    status: str
