from utils import websocket
from utils import resource_notify
from fastapi.websockets import WebSocket
import json
import asyncio
from shelljob import proc
from services.TrackingService import TrackingService
from threading import Thread


class SocketService:
    manager = websocket.ConnectionManager(resource_notify.loop_to_notify_resource)
    command_task = {}

    # Router event
    @classmethod
    async def execute_event(cls, user_id: str, data: str):
        # Parse the data
        data = json.loads(data)
        # Selection event function
        if type(data) is dict and "event" in data and hasattr(cls, data["event"]):
            print(f">> New request from {user_id}: {data['event']}")
            event_func = getattr(cls, data["event"])
            asyncio.get_event_loop().create_task(event_func(user_id, data["data"]))

    # Process event
    @classmethod
    async def update_group(cls, user_id: str, data: dict):
        if "groups" in data:
            cls.manager.update_group(user_id, data["groups"])

    @classmethod
    async def execute_command(cls, user_id: str, data: dict):
        cls.command_task[user_id] = asyncio.get_event_loop().create_task(cls.create_command_task(user_id, data))
        # Tracking
        Thread(target=lambda: TrackingService.add_action(user_id, f"Execute command  {str(data)}")).start()
        # End tracking
    
    @classmethod
    async def cancel_command(cls, user_id: str, data: dict):
        if user_id in cls.command_task:
            cls.command_task[user_id].cancel()
        data = {
            "event": "response_command",
            "data": {
                "command": "Task was cancel!"
            }

        }
        asyncio.get_event_loop().create_task(cls.manager.unicast(user_id, data))
    
    @classmethod    
    async def create_command_task(cls, user_id: str, data: dict):
        if "command" in data:
            cwd = "./" if "cwd" not in data else data["cwd"]
            g = proc.Group()
            p = g.run([data["command"]], shell=True)
            while g.is_pending():
                lines = g.readlines()
                for _, line in lines:
                    data = {
                        "event": "response_command",
                        "data": {
                            "command": line.decode("utf-8")
                        }

                    }
                    asyncio.get_event_loop().create_task(cls.manager.unicast(user_id, data))
                    await asyncio.sleep(0.01)

    # Connection management
    @classmethod
    async def add_connection(cls, user_id: str, socket: WebSocket, data: dict):
        await cls.manager.add_connection(user_id, socket, data)

    @classmethod
    async def disconnect(cls, user_id: str):
        cls.manager.disconnect(user_id)
