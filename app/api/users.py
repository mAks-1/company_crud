from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User, db_helper
from app.core.schemas.schemas import ReadUser, CreateUser, DeleteUser, UpdateUser
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


@router.get("/{user_id}", response_model=ReadUser)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id_to_get: int,
):
    user = await crud_users.get_user_by_id(
        session=session,
        user_id_to_get=user_id_to_get,
    )

    return user if user else None


@router.delete("/{user_id}", response_model=DeleteUser)
async def delete_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id_to_delete: int,
):
    user = await crud_users.delete_user_by_id(
        session=session,
        user_id_to_delete=user_id_to_delete,
    )
    return user if user else None


@router.patch("/{user_id}", response_model=ReadUser)
async def update_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_update: UpdateUser,
    user_id_to_update: int,
):
    result = await crud_users.update_user_by_id(
        session=session,
        user_to_update=user_update,
        user_id_to_update=user_id_to_update,
    )
    return result if result else None
