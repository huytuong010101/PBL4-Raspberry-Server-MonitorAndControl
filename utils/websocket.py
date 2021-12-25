from fastapi.websockets import WebSocket, WebSocketDisconnect
import asyncio


class ConnectionManager:
    def __init__(self, loop_task=None):
        self.connections = {}
        if loop_task is not None:
            print(">> Start notify loop")
            asyncio.get_event_loop().create_task(loop_task(self.multicast))

    def add_group(self, user_id: str, new_group: str):
        if user_id in self.connections:
            self.connections[user_id]["groups"].append(new_group)

    def remove_group(self, user_id: str, group: str):
        if user_id in self.connections:
            self.connections[user_id]["groups"].remove(group)

    def update_group(self, user_id: str, groups: dict):
        if user_id in self.connections:
            self.connections[user_id]["groups"] = groups

    async def add_connection(self, user_id: str, conn: WebSocket, data: dict = None):
        self.connections[user_id] = {
            "ws": conn,
            "groups": []
        }
        if data is not None:
            self.connections[user_id].update(data)
        print(f">> Add {user_id} to manage socket")

    async def multicast(self, message: dict, group: str = None):
        for user_id in self.connections:
            if group is None or group in self.connections[user_id]["groups"]:
                await self.connections[user_id]["ws"].send_json(message)

    async def broadcast(self, message: dict):
        for user_id in self.connections:
            await self.connections[user_id]["ws"].send_json(message)

    async def unicast(self, user_id: str, message: dict):
        await self.connections[user_id]["ws"].send_json(message)

    def disconnect(self, user_id: str):
        if self.connections.get(user_id):
            del self.connections[user_id]
        print(f">> Remove socket of {user_id}")
