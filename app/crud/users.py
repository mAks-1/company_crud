from typing import Sequence, Optional
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import User
from app.core.schemas.schemas import CreateUser, UpdateUser
from app.auth.auth_password import hash_password


async def create_user(
    session: AsyncSession,
    user_create: CreateUser,
) -> User:
    # Check if username already exists
    existing_user = await get_user_by_username(session, user_create.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    # Hash the password
    hashed_password = hash_password(user_create.password)

    # Create user data dict
    user_data = user_create.model_dump(exclude={"password"})
    user_data["password_hash"] = hashed_password

    user = User(**user_data)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_users(session: AsyncSession) -> Sequence[User]:
    result = await session.execute(select(User).order_by(User.user_id))
    return result.scalars().all()


async def get_user_by_id(
    session: AsyncSession,
    user_id_to_get: int,
) -> User:
    result = await session.execute(select(User).where(User.user_id == user_id_to_get))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_user_by_username(
    session: AsyncSession,
    user_username_to_get: str,
) -> Optional[User]:
    result = await session.execute(
        select(User).where(User.username == user_username_to_get)
    )
    return result.scalars().first()


async def delete_user_by_id(
    session: AsyncSession,
    user_id_to_delete: int,
) -> dict:
    user = await get_user_by_id(session, user_id_to_delete)
    await session.delete(user)
    await session.commit()
    return {"message": "User deleted successfully"}


async def update_user_by_id(
    session: AsyncSession,
    user_id_to_update: int,
    update_data: UpdateUser,
) -> User:
    user = await get_user_by_id(session, user_id_to_update)

    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))

    # for field, value in update_data.items():
    #     if hasattr(user, field) and value is not None:
    #         setattr(user, field, value)

    if update_data.username is not None:
        user.username = update_data.username
    if update_data.email is not None:
        user.email = update_data.email
    if update_data.first_name is not None:
        user.first_name = update_data.first_name
    if update_data.last_name is not None:
        user.last_name = update_data.last_name
    if update_data.company_id is not None:
        user.company_id = update_data.company_id
    if update_data.password is not None:
        user.password = update_data.password

    await session.commit()
    await session.refresh(user)
    return user
