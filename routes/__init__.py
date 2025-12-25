from .camera import router as camera_router
from .auth import router as auth_router

__all__ = ["auth_router", "camera_router"]
