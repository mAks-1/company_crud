from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Form, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper
from app.core.schemas.schemas import ReadUser, CreateUser, DeleteUser, UpdateUser
from app.crud import users as crud_users


from app.auth import auth_validation as auth_validation
from app.auth import jwt as auth_jwt
from app.api.jwt import TokenInfo
from app.auth import auth_password as auth_password


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=list[ReadUser])
async def get_users(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    users = await crud_users.get_users(session=session)
    return users


# JUST FOR DEVELOPING
@router.post("/", response_model=ReadUser, status_code=status.HTTP_201_CREATED)
async def create_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_data: CreateUser,
):
    return await crud_users.create_user(session=session, user_create=user_data)


@router.get("/{user_id}", response_model=ReadUser)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id: int,
):
    user = await crud_users.get_user_by_id(
        session=session,
        user_id_to_get=user_id,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get("/usernames/{username}", response_model=ReadUser)
async def get_user_by_username(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    username: str,
):
    user = await crud_users.get_user_by_username(
        session=session,
        user_username_to_get=username,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.delete("/{user_id}", response_model=DeleteUser)
async def delete_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id: int,
):
    user = await crud_users.delete_user_by_id(
        session=session,
        user_id_to_delete=user_id,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"message": f"User with id {user_id} deleted successfully"}


@router.patch("/{user_id}", response_model=ReadUser)
async def update_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id: int,
    user_update: UpdateUser,
):
    update_data = user_update.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password_hash"] = auth_password.hash_password(
            update_data.pop("password")
        )

    user = await crud_users.update_user_by_id(
        session=session,
        user_id_to_update=user_id,
        update_data=user_update,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/login/", response_model=TokenInfo)
async def auth_user_issue_jwt(
    session: AsyncSession = Depends(db_helper.session_getter),
    username: str = Form(),
    password: str = Form(),
):
    user = await auth_validation.validate_auth_user_from_db(
        session=session,
        username=username,
        password=password,
    )

    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = auth_jwt.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


# FOR REAL REGISTRATION
@router.post("/register/", response_model=ReadUser)
async def register_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_data: CreateUser,
):
    # Check if user exists
    try:
        existing = await crud_users.get_user_by_username(
            session=session,
            user_username_to_get=user_data.username,
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Username already exists",
            )
    except HTTPException as e:
        if e.status_code != 404:
            raise

    # Create user
    user = await crud_users.create_user(
        session=session,
        user_create=user_data,
    )
    return user
