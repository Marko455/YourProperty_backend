from fastapi import APIRouter, Depends
from shared.auth.jwt_dependency import verify_token
from shared.db.dynamodb import get_table
from app.models.user_models import UserProfile, FavoritesUpdate

router = APIRouter()
table = get_table("UserProfiles")

@router.post("/profile")
def create_or_update_profile(
    data: UserProfile,
    user_id: str = Depends(verify_token)
):
    table.put_item(
        Item={
            "user_id": user_id,
            "name": data.name,
            "phone": data.phone,
            "role": data.role,
            "favorites": []
        }
    )
    return {"message": "Profile saved"}

@router.get("/profile")
def get_profile(user_id: str = Depends(verify_token)):
    response = table.get_item(Key={"user_id": user_id})
    return response.get("Item")

@router.post("/favorites")
def add_favorite(
    data: FavoritesUpdate,
    user_id: str = Depends(verify_token)
):
    table.update_item(
        Key={"user_id": user_id},
        UpdateExpression="ADD favorites :f",
        ExpressionAttributeValues={":f": {data.listing_id}}
    )
    return {"message": "Favorite added"}
