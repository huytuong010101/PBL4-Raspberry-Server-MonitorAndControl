from fastapi import APIRouter
from fastapi.websockets import WebSocketDisconnect, WebSocket
from utils import websocket
from utils import resource_notify

socket_router = APIRouter(tags=["Socket manager"])
manager = websocket.ConnectionManager(resource_notify.loop_to_notify_resource)


@socket_router.websocket("/{user_id}")
async def websocket_endpoint(ws: WebSocket, user_id: int):
    await ws.accept()
    await manager.add_connection(user_id, ws, {})
    try:
        while True:
            data = await ws.receive_text()
            print(">> Receive from socket:", str(data))
    except WebSocketDisconnect:
        print(f">> Disconnect to {user_id}:")
        manager.disconnect(user_id)
