from fastapi import APIRouter, Depends
import uuid, datetime

from shared.auth.jwt_dependency import verify_token
from shared.db.dynamodb import get_table
from app.models.listing_models import ListingCreate

router = APIRouter()
table = get_table("Listings")

@router.post("/")
def create_listing(
    data: ListingCreate,
    user_id: str = Depends(verify_token)
):
    listing_id = str(uuid.uuid4())

    table.put_item(
        Item={
            "listing_id": listing_id,
            "owner_id": user_id,
            "title": data.title,
            "description": data.description,
            "price": data.price,
            "city": data.city,
            "property_type": data.property_type,
            "status": "active",
            "created_at": datetime.datetime.utcnow().isoformat()
        }
    )
    return {"listing_id": listing_id}

@router.get("/city/{city}")
def get_by_city(city: str):
    response = table.query(
        IndexName="city-price-index",
        KeyConditionExpression="city = :c",
        ExpressionAttributeValues={":c": city}
    )
    return response["Items"]
