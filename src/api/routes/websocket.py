from fastapi import APIRouter, WebSocket

from src.infrastructure.websocket.connection import WebSocketManager

router = APIRouter()
ws_manager = WebSocketManager()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str,
):
    await ws_manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except:
        await ws_manager.disconnect(user_id, websocket)
