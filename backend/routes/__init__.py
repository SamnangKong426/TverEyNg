from .stream import router as stream_router
# from .yolo import router as yolo_router
from .camera import router as camera_router

__all__ = [
    # "yolo_router",
    "stream_router",
    "camera_router"
]