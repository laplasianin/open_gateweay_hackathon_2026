from pydantic import BaseModel


class WsMessage(BaseModel):
    type: str
    data: dict
