from fastapi import APIRouter
from fastapi.websockets import WebSocketDisconnect, WebSocket
from utils import websocket
from utils import resource_notify

socket_router = APIRouter(tags=["Computer resource"])
manager = websocket.ConnectionManager(resource_notify.loop_to_notify_resource)


@socket_router.websocket("/resource")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            data = await ws.receive_text()
            print(">> Receive from socket:", str(data))
    except WebSocketDisconnect:
        manager.disconnect(ws)
