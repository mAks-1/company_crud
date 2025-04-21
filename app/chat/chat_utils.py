from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.models import Message
from datetime import datetime


async def save_message(session: AsyncSession, user_id: int, content: str):
    message = Message(user_id=user_id, content=content, timestamp=datetime.utcnow())
    session.add(message)
    await session.commit()


async def get_last_messages(session: AsyncSession, limit: int = 20):
    result = await session.execute(
        select(Message)
        .options(selectinload(Message.user))
        .order_by(Message.timestamp.desc())
        .limit(limit)
    )
    return reversed(result.scalars().all())
