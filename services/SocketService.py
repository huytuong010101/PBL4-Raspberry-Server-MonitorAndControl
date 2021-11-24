from utils import websocket
from utils import resource_notify
from fastapi.websockets import WebSocket
import json
import asyncio
from shelljob import proc
from services.TrackingService import TrackingService
from threading import Thread
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('127.0.0.1', username='pi', password='pi')


class SocketService:
    manager = websocket.ConnectionManager(resource_notify.loop_to_notify_resource)
    command_task = {}
    session = {}

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
    async def connect_ssh(cls, user_id: str, data: dict):
        # init session if not yet
        if user_id in cls.session:
            cls.session[user_id].close()
        cls.session[user_id] = ssh.invoke_shell()
        await asyncio.sleep(0.3)
        while cls.session[user_id].recv_ready():
            data = {
                "event": "response_command",
                "data": {
                    "command": cls.session[user_id].recv(1024).decode("utf-8")
                }

            }
            asyncio.get_event_loop().create_task(cls.manager.unicast(user_id, data))

    @classmethod
    async def execute_command(cls, user_id: str, data: dict):
        # start a command
        cls.command_task[user_id] = asyncio.get_event_loop().create_task(cls.create_command_task(user_id, data))
        # Tracking
        Thread(target=lambda: TrackingService.add_action(user_id, f"Execute command  {str(data)}")).start()
        # End tracking
    
    @classmethod
    async def cancel_command(cls, user_id: str, data: dict):
        if user_id in cls.command_task:
            cls.command_task[user_id].cancel()
        if user_id in cls.session:
            cls.session[user_id].close()
        cls.session[user_id] = ssh.invoke_shell()
        if cls.session[user_id].recv_ready():
            data = {
                "event": "response_command",
                "data": {
                    "command": cls.session[user_id].recv(1024).decode("utf-8")
                }

            }
            asyncio.get_event_loop().create_task(cls.manager.unicast(user_id, data))
    
    @classmethod    
    async def create_command_task(cls, user_id: str, data: dict):
        if "command" in data:
            cwd = "./" if "cwd" not in data else data["cwd"]
            while cls.session[user_id].recv_ready(): cls.session[user_id].recv(1024)
            cls.session[user_id].send(data["command"] + "\n")
            while True:
                if cls.session[user_id].recv_ready():
                    receive = cls.session[user_id].recv(1024).decode("utf-8")
                    print(receive)
                    data = {
                        "event": "response_command",
                        "data": {
                            "command": receive
                        }

                    }
                    asyncio.get_event_loop().create_task(cls.manager.unicast(user_id, data))
                    await asyncio.sleep(0.01)
                    if "pi@pi" in receive or receive.strip("\n").strip() == "":
                        break

    # Connection management
    @classmethod
    async def add_connection(cls, user_id: str, socket: WebSocket, data: dict):
        await cls.manager.add_connection(user_id, socket, data)

    @classmethod
    async def disconnect(cls, user_id: str):
        cls.manager.disconnect(user_id)
        if user_id in cls.command_task:
            cls.command_task[user_id].cancel()
        if user_id in cls.session:
            cls.session[user_id].close()
