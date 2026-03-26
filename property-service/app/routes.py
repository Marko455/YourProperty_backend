from fastapi import APIRouter, HTTPException, UploadFile, File
from models import PropertyCreate, PropertyUpdate
from db import get_table
import uuid
import shutil
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

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
    expr_names = {}

    for field, value in update.dict(exclude_unset=True).items():
        placeholder_name = f"#{field}"
        placeholder_value = f":{field}"

        update_expr.append(f"{placeholder_name} = {placeholder_value}")
        expr_values[placeholder_value] = value
        expr_names[placeholder_name] = field

    if not update_expr:
        raise HTTPException(status_code=400, detail="No fields to update")

    table.update_item(
        Key={"property_id": property_id},
        UpdateExpression="SET " + ", ".join(update_expr),
        ExpressionAttributeValues=expr_values,
        ExpressionAttributeNames=expr_names
    )

    return {"message": "Property updated"}


@router.delete("/{property_id}")
def delete_property(property_id: str):
    table.delete_item(Key={"property_id": property_id})
    return {"message": "Property deleted"}

@router.post("/{property_id}/images")
async def upload_property_images(
    property_id: str,
    files: list[UploadFile] = File(...)
):
    response = table.get_item(Key={"property_id": property_id})
    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Property not found")

    image_urls = []

    for file in files:
        filename = f"{uuid.uuid4()}-{file.filename}"
        filepath = UPLOAD_DIR / filename

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        image_url = f"/uploads/{filename}"
        image_urls.append(image_url)

    table.update_item(
        Key={"property_id": property_id},
        UpdateExpression="SET images = list_append(if_not_exists(images, :empty), :imgs)",
        ExpressionAttributeValues={
            ":imgs": image_urls,
            ":empty": []
        }
    )

    return {
        "message": "Images uploaded",
        "property_id": property_id,
        "images": image_urls
    }

@router.delete("/{property_id}/images")
def delete_property_image(property_id: str, image_url: str):
    response = table.get_item(Key={"property_id": property_id})
    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Property not found")

    property_item = response["Item"]
    images = property_item.get("images", [])

    if image_url not in images:
        raise HTTPException(status_code=404, detail="Image not found")

    updated_images = [img for img in images if img != image_url]

    table.update_item(
        Key={"property_id": property_id},
        UpdateExpression="SET images = :imgs",
        ExpressionAttributeValues={
            ":imgs": updated_images
        }
    )

    return {"message": "Image removed"}