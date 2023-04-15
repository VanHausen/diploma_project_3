from pydantic import BaseModel, Field


class MessageFrom(BaseModel):
    id: int
    username: str | None = None

class Chat(BaseModel):
    id: int
    username: str | None = None

class Message(BaseModel):
    message_id: int
    from_: MessageFrom = Field(..., alias='from')
    chat=Chat
    text: str | None = None

class UpdateObj:
    update_id: int
    message: Message


class SendMessageResponse(BaseModel):
    ok: bool
    result: Message


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: list[UpdateObj] = []

    class Config:
        arbitrary_types_allowed = True