from abc import ABC, abstractmethod


class NokiaClient(ABC):
    @abstractmethod
    async def create_qod_session(self, device_id: str, profile: str, duration: int | None) -> str:
        ...

    @abstractmethod
    async def delete_qod_session(self, session_id: str) -> bool:
        ...
