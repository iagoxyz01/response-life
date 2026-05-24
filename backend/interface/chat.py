from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from infrastructure.database import get_db
from infrastructure.models import UsuarioModel
from typing import Dict, List
import json

router = APIRouter(prefix="/chat", tags=["Chat"])

# Gerenciador de conexões ativas
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)

    async def broadcast(self, message: dict, room_id: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_text(json.dumps(message))


manager = ConnectionManager()


# Modelo de mensagem para salvar no banco
class MensagemCreate(BaseModel):
    destinatario_id: int
    texto: str


class MensagemResponse(BaseModel):
    id: int
    remetente_id: int
    destinatario_id: int
    texto: str
    criado_em: str

    class Config:
        from_attributes = True


@router.websocket("/ws/{room_id}/{usuario_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    usuario_id: int,
):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            message["usuario_id"] = usuario_id
            await manager.broadcast(message, room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)