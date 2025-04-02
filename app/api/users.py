from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User, db_helper
from app.core.schemas.schemas import ReadUser, CreateUser
from app.crud import users as crud_users

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=list[ReadUser])
async def get_users(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    users = await crud_users.get_users(session=session)
    return users if users else []


@router.post("/", response_model=ReadUser)
async def create_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_create: CreateUser,
):
    return await crud_users.create_user(
        session=session,
        user_create=user_create,
    )
