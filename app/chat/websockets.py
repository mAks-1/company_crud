from fastapi import APIRouter, WebSocket


router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
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
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    pass
