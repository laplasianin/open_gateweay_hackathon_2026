from app.config import settings
from app.nokia.base import NokiaClient
from app.nokia.mock import MockNokiaClient
from app.nokia.real import RealNokiaClient

_client: NokiaClient | None = None


def get_nokia_client() -> NokiaClient:
    global _client
    if _client is None:
        if settings.nokia_mode == "real":
            _client = RealNokiaClient(settings.nokia_api_key, settings.nokia_api_secret)
        else:
            _client = MockNokiaClient()
    return _client


async def activate_qod(device_id: str, role: str) -> str:
    client = get_nokia_client()
    if role == "vip":
        return await client.create_qod_session(device_id, "QOS_M", duration=900)
    else:
        return await client.create_qod_session(device_id, "QOS_L", duration=None)


async def deactivate_qod(session_id: str) -> bool:
    client = get_nokia_client()
    return await client.delete_qod_session(session_id)
