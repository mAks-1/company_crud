from typing import Annotated

from fastapi import APIRouter, WebSocket, Depends, status

from jwt.exceptions import InvalidTokenError
from requests import session
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper
from app.auth import jwt as jwt_utils
from app.crud import users as crud_users
from app.chat.chat_utils import save_message, get_last_messages

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, personal_message: str, websocket: WebSocket):
        await websocket.send_text(personal_message)

    async def broadcast(self, personal_message: str):
        for connection in self.active_connections:
            await connection.send_text(personal_message)


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    websocket: WebSocket,
):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        payload = jwt_utils.decode_jwt(token)
    except InvalidTokenError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    username = payload.get("sub")
    if not username:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user = await crud_users.get_user_by_username(
        session=session, user_username_to_get=username
    )
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()

    await manager.connect(websocket)

    last_messages = await get_last_messages(session)
    for msg in last_messages:
        await websocket.send_text(f"{msg.user.username}: {msg.content}")

    try:
        while True:
            data = await websocket.receive_text()

            await save_message(session=session, user_id=user.user_id, content=data)

            await manager.broadcast(f"{user.username}: {data}")
    except Exception as e:
        print("Connection closed:", e)
    finally:
        manager.disconnect(websocket)
