from fastapi.websockets import WebSocket, WebSocketDisconnect
from typing import List
import asyncio


class ConnectionManager:
    def __init__(self, loop_task=None):
        self.connections = {}
        if loop_task is not None:
            print(">> Start notify loop")
            asyncio.get_event_loop().create_task(loop_task(self.broadcast))

    async def add_connection(self, user_id: int,conn: WebSocket, data: dict = None):
        self.connections[user_id] = {
            "ws": conn,
        }
        if data is not None:
            self.connections[user_id].update(data)
        print(f">> Add {user_id} to manage socket")

    async def broadcast(self, message: dict):
        for user_id in self.connections:
            await self.connections[user_id]["ws"].send_json(message)

    def disconnect(self, user_id: int):
        if self.connections.get(user_id):
            del self.connections[user_id]
        print(f">> Remove socket of {user_id}")
