from fastapi import Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth_password import validate_password
from app.crud import users as crud_users


async def validate_auth_user_from_db(
    session: AsyncSession,
    username: str = Form(),
    password: str = Form(),
):
    user = await crud_users.get_user_by_username(
        session=session, user_username_to_get=username
    )

    if not user or not validate_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return user
