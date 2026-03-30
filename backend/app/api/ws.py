from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.ws_manager import ws_manager

router = APIRouter()


@router.websocket("/ws/events/{event_id}")
async def event_websocket(websocket: WebSocket, event_id: str):
    await ws_manager.connect(event_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(event_id, websocket)
