from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User
from app.core.schemas.schemas import CreateUser, UpdateUser


async def create_user(
    session: AsyncSession,
    user_create: CreateUser,
) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    return user


async def get_users(
    session: AsyncSession,
) -> Sequence[User]:
    stmt = select(User).order_by(User.user_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_user_by_id(
    session: AsyncSession,
    user_id_to_get: int,
) -> User:
    result = await session.execute(
        select(User).filter(User.user_id == user_id_to_get),
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def delete_user_by_id(
    session: AsyncSession,
    user_id_to_delete: int,
) -> dict:
    result = await session.execute(
        select(User).filter(User.user_id == user_id_to_delete),
    )

    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()
    return {"message": "User deleted successfully"}


async def update_user_by_id(
    session: AsyncSession,
    user_to_update: UpdateUser,
    user_id_to_update: int,
) -> User:
    result = await session.execute(
        select(User).filter(User.user_id == user_id_to_update),
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_to_update.first_name is not None:
        user.first_name = user_to_update.first_name
    if user_to_update.last_name is not None:
        user.last_name = user_to_update.last_name
    if user_to_update.email is not None:
        user.email = user_to_update.email
    if user_to_update.company_id is not None:
        user.company_id = user_to_update.company_id

    await session.commit()
    await session.refresh(user)
    return user
