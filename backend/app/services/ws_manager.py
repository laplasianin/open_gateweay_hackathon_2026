import json
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self._connections: dict[str, list[WebSocket]] = {}

    async def connect(self, event_id: str, websocket: WebSocket):
        await websocket.accept()
        if event_id not in self._connections:
            self._connections[event_id] = []
        self._connections[event_id].append(websocket)

    def disconnect(self, event_id: str, websocket: WebSocket):
        if event_id in self._connections:
            self._connections[event_id].remove(websocket)

    async def broadcast(self, event_id: str, message: dict):
        if event_id not in self._connections:
            return
        dead = []
        for ws in self._connections[event_id]:
            try:
                await ws.send_text(json.dumps(message))
            except Exception:
                dead.append(ws)
        for ws in dead:
            self._connections[event_id].remove(ws)


ws_manager = ConnectionManager()
