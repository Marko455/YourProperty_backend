from fastapi import APIRouter, Depends, HTTPException
from models import InquiryCreate, InquiryUpdate
from db import get_table
from auth import get_current_user
import uuid
from datetime import datetime

router = APIRouter(prefix="/inquiries", tags=["Inquiries"])
table = get_table()

@router.post("/")
def create_inquiry(
    inquiry: InquiryCreate,
    user=Depends(get_current_user)
):
    if user["role"] != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can create inquiries")

    item = {
        "inquiry_id": str(uuid.uuid4()),
        "property_id": inquiry.property_id,
        "buyer_id": user["user_id"],
        "message": inquiry.message,
        "status": "open",
        "created_at": datetime.utcnow().isoformat()
    }

    table.put_item(Item=item)
    return item


@router.get("/me")
def get_my_inquiries(user=Depends(get_current_user)):
    if user["role"] != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can view this")

    response = table.scan(
        FilterExpression="buyer_id = :b",
        ExpressionAttributeValues={":b": user["user_id"]}
    )

    return response.get("Items", [])


@router.get("/property/{property_id}")
def get_property_inquiries(
    property_id: str,
    user=Depends(get_current_user)
):
    if user["role"] != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can view property inquiries")

    response = table.scan(
        FilterExpression="property_id = :p",
        ExpressionAttributeValues={":p": property_id}
    )

    return response.get("Items", [])


@router.put("/{inquiry_id}")
def update_inquiry(
    inquiry_id: str,
    update: InquiryUpdate,
    user=Depends(get_current_user)
):
    if user["role"] != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can update inquiries")

    table.update_item(
        Key={"inquiry_id": inquiry_id},
        UpdateExpression="SET #s = :s",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": update.status}
    )

    return {"message": "Inquiry updated"}

@router.post("/inquiries")
def create_inquiry(
    inquiry: InquiryCreate,
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can send inquiries")

    item = {
        "inquiry_id": str(uuid.uuid4()),
        "property_id": inquiry.property_id,
        "seller_id": inquiry.seller_id,
        "buyer_id": current_user["user_id"],
        "message": inquiry.message,
        "created_at": datetime.utcnow().isoformat(),
    }

    table.put_item(Item=item)
    return {"message": "Inquiry sent"}

@router.get("/inquiries/my")
def get_my_inquiries(current_user=Depends(get_current_user)):
    if current_user["role"] != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can view inquiries")

    response = table.scan(
        FilterExpression="seller_id = :sid",
        ExpressionAttributeValues={":sid": current_user["user_id"]}
    )

    return response.get("Items", [])