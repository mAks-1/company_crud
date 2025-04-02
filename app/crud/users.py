from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User
from app.core.schemas.schemas import CreateUser


async def create_user(
    session: AsyncSession,
    user_create: CreateUser,
):
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
