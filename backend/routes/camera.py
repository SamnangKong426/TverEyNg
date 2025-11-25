from fastapi import APIRouter
from sqlmodel import select
from models import Camera
from config.db import Session, engine

router = APIRouter()

@router.post("/", response_model=Camera)
async def create_camera(camera: Camera):
    with Session(engine) as session:
        session.add(camera)
        session.commit()
        session.refresh(camera)
        return camera

@router.get("/")
async def read_cameras():
    with Session(engine) as session:
        cameras = session.exec(select(Camera)).all()
        return cameras

