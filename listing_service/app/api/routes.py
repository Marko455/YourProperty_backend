from fastapi import APIRouter, Depends, HTTPException
from shared.auth.dependencies import get_current_user
from app.schemas.listing import (
    PropertyCreate,
    PropertyUpdate,
    PropertyOut,
)
from app.services.listing_service import ListingService

router = APIRouter(prefix="/properties", tags=["properties"])

@router.post("/", response_model=PropertyOut)
def create_property(
    data: PropertyCreate,
    user_id: str = Depends(get_current_user),
):
    return ListingService.create(data.model_dump(), user_id)

@router.get("/{property_id}", response_model=PropertyOut)
def get_property(property_id: str):
    item = ListingService.get(property_id)
    if not item:
        raise HTTPException(404, "Not found")
    return item

@router.get("/", response_model=list[PropertyOut])
def list_properties(city: str):
    return ListingService.list_by_city(city)

@router.put("/{property_id}")
def update_property(
    property_id: str,
    data: PropertyUpdate,
    user_id: str = Depends(get_current_user),
):
    try:
        ListingService.update(
            property_id,
            user_id,
            data.model_dump(exclude_unset=True),
        )
        return {"message": "Updated"}
    except PermissionError:
        raise HTTPException(403, "Forbidden")

@router.delete("/{property_id}")
def delete_property(
    property_id: str,
    user_id: str = Depends(get_current_user),
):
    try:
        ListingService.delete(property_id, user_id)
        return {"message": "Deleted"}
    except PermissionError:
        raise HTTPException(403, "Forbidden")
