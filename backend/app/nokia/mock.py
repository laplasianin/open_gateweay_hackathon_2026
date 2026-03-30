import asyncio
import random
import uuid
from datetime import datetime, timezone

from app.nokia.base import NokiaClient


class MockNokiaClient(NokiaClient):
    def __init__(self):
        self.call_log: list[dict] = []
        self._sessions: set[str] = set()

    async def create_qod_session(self, device_id: str, profile: str, duration: int | None) -> str:
        await asyncio.sleep(random.uniform(0.2, 0.5))
        session_id = f"fake-session-{uuid.uuid4().hex[:12]}"
        self._sessions.add(session_id)
        self.call_log.append({
            "action": "create_qod_session",
            "device_id": device_id,
            "profile": profile,
            "duration": duration,
            "session_id": session_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return session_id

    async def delete_qod_session(self, session_id: str) -> bool:
        await asyncio.sleep(random.uniform(0.1, 0.3))
        self._sessions.discard(session_id)
        self.call_log.append({
            "action": "delete_qod_session",
            "session_id": session_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return True
