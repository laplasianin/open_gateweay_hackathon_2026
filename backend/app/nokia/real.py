from app.nokia.base import NokiaClient


class RealNokiaClient(NokiaClient):
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    async def create_qod_session(self, device_id: str, profile: str, duration: int | None) -> str:
        raise NotImplementedError("Real Nokia client not yet configured — set NOKIA_MODE=mock")

    async def delete_qod_session(self, session_id: str) -> bool:
        raise NotImplementedError("Real Nokia client not yet configured — set NOKIA_MODE=mock")
