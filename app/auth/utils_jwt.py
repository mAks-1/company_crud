from datetime import timedelta, datetime
import bcrypt
import jwt
from fastapi import Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.crud import users as crud_users


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm=settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expires_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key=settings.auth_jwt.public_key_path.read_text(),
    algorithm=settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(
    password: str,
) -> str:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def validate_password(
    password: str,
    hashed_password: str,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode(),
    )


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
