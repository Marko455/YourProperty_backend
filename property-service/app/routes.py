from fastapi import APIRouter, HTTPException
from models import PropertyCreate, PropertyUpdate
from db import get_table
import uuid
from datetime import datetime

router = APIRouter(prefix="/properties", tags=["Properties"])

table = get_table()

@router.post("/")
def create_property(property: PropertyCreate):
    property_id = str(uuid.uuid4())

    item = {
        "property_id": property_id,
        "owner_id": property.owner_id,
        "title": property.title,
        "description": property.description,
        "rooms": property.rooms,
        "bathrooms": property.bathrooms,
        "bedrooms": property.bedrooms,
        "parking_spots": property.parking_spots,
        "price": property.price,
        "location": property.location,
        "type": property.type,
        "created_at": datetime.utcnow().isoformat()
    }

    table.put_item(Item=item)
    return item


@router.get("/")
def list_properties():
    response = table.scan()
    return response.get("Items", [])


@router.get("/{property_id}")
def get_property(property_id: str):
    response = table.get_item(Key={"property_id": property_id})

    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Property not found")

    return response["Item"]


@router.put("/{property_id}")
def update_property(property_id: str, update: PropertyUpdate):
    update_expr = []
    expr_values = {}

    for field, value in update.dict(exclude_unset=True).items():
        update_expr.append(f"{field} = :{field}")
        expr_values[f":{field}"] = value

    if not update_expr:
        raise HTTPException(status_code=400, detail="No fields to update")

    table.update_item(
        Key={"property_id": property_id},
        UpdateExpression="SET " + ", ".join(update_expr),
        ExpressionAttributeValues=expr_values
    )

    return {"message": "Property updated"}


@router.delete("/{property_id}")
def delete_property(property_id: str):
    table.delete_item(Key={"property_id": property_id})
    return {"message": "Property deleted"}
