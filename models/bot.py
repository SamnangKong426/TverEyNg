from pydantic import BaseModel


class BotSchema(BaseModel):
    user_id: int
    bot_token: str
    chat_id: str


class BotUpdateSchema(BaseModel):
    bot_token: str | None = None
    chat_id: str | None = None
