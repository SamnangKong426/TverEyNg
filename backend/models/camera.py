from datetime import datetime
from sqlmodel import SQLModel, Field

class Camera(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str  
    ip_address: str
    is_online: bool = False 
    location: str | None = None   
