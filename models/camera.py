from pydantic import BaseModel


class CameraSchema(BaseModel):
    name: str
    ip: str
