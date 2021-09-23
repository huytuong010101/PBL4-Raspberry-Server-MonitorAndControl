from fastapi.websockets import WebSocket, WebSocketDisconnect
from typing import List
import asyncio


class ConnectionManager:
    def __init__(self, loop_task=None):
        self.active_connections: List[WebSocket] = []
        if loop_task is not None:
            print(">> Start notify loop")
            asyncio.get_event_loop().create_task(loop_task(self.broadcast))

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)