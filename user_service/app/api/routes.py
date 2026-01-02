from fastapi import APIRouter, Depends, HTTPException
from shared.auth.dependencies import get_current_user
from app.schemas.user import UserProfile, UserProfileUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserProfile)
def get_me(user_id: str = Depends(get_current_user)):
    profile = UserService.get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")

    return profile

@router.put("/me")
def update_me(
    data: UserProfileUpdate,
    user_id: str = Depends(get_current_user),
):
    UserService.update_profile(
        user_id,
        data.model_dump(exclude_unset=True),
    )
    return {"message": "Profile updated"}
