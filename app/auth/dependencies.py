from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import db_helper, User
from app.core.schemas.schemas import UserSchema
from app.auth import jwt as jwt_utils
from app.crud import users as crud_users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login/")


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = jwt_utils.decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return payload


async def get_current_auth_user(
    session: AsyncSession = Depends(db_helper.session_getter),
    payload: dict = Depends(get_current_token_payload),
) -> User:
    username: str = payload.get("sub")
    user = await crud_users.get_user_by_username(session, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return user


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    # if user.active:
    #     return user
    # raise HTTPException(
    #     status_code=status.HTTP_403_FORBIDDEN,
    #     detail="inactive user",
    # )

    return user
