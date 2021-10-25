from utils import websocket
from utils import resource_notify
from fastapi.websockets import WebSocket
import json
import subprocess


class SocketService:
    manager = websocket.ConnectionManager(resource_notify.loop_to_notify_resource)

    # Router event
    @classmethod
    async def execute_event(cls, user_id: int, data: str):
        # Parse the data
        data = json.loads(data)
        # Selection event function
        if type(data) is dict and "event" in data and hasattr(cls, data["event"]):
            print(f">> New request from {user_id}: {data['event']}")
            event_func = getattr(cls, data["event"])
            await event_func(user_id, data["data"])

    # Process event
    @classmethod
    async def update_group(cls, user_id: int, data: dict):
        if "groups" in data:
            cls.manager.update_group(user_id, data["groups"])

    @classmethod
    async def execute_command(cls, user_id: int, data: dict):
        if "command" in data:
            cwd = "./" if "cwd" not in data else data["cwd"]
            output = subprocess.run(data["command"], cwd=cwd, shell=True, capture_output=True, text=True).stdout
            data = {
                "event": "response_command",
                "response": output
            }
            await cls.manager.unicast(user_id, data)

    # Connection management
    @classmethod
    async def add_connection(cls, user_id: int, socket: WebSocket, data: dict):
        await cls.manager.add_connection(user_id, socket, data)

    @classmethod
    async def disconnect(cls, user_id: int):
        cls.manager.disconnect(user_id)
