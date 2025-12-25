from pydantic import BaseModel


class CameraSchema(BaseModel):
    name: str
    ip: str
    user_id: int
