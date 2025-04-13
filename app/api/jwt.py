from datetime import datetime
from fastapi import APIRouter, Depends
from app.core.schemas.schemas import UserSchema, UserBase
from app.auth.dependencies import (
    get_current_active_auth_user,
    get_current_token_payload,
)
from pydantic import BaseModel

router = APIRouter(
    prefix="/jwt",
    tags=["jwt"],
)


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


@router.get("/users/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserBase = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "active": user.active,
        "role": user.role,
        "email": user.email,
        "logged_in_at": datetime.utcfromtimestamp(iat).isoformat() if iat else None,
    }
