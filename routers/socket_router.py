from fastapi import APIRouter
from fastapi.websockets import WebSocketDisconnect, WebSocket
from services.SocketService import SocketService
from utils.auth import AuthUtil

socket_router = APIRouter(tags=["Socket manager"])


@socket_router.websocket("/{token}")
async def websocket_endpoint(ws: WebSocket, token: str):
    user = None
    try:
        user = AuthUtil.decode_token(token)
    except Exception:
        return
    user_id = user["sub"]
    await ws.accept()
    await SocketService.add_connection(user_id, ws, {"groups": "resource"})
    try:
        while True:
            data = await ws.receive_text()
            await SocketService.execute_event(user_id, data)
    except WebSocketDisconnect:
        print(f">> Disconnect to {user_id}:")
        await SocketService.disconnect(user_id)


