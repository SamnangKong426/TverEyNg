from fastapi import FastAPI

from routes import camera_router, user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(camera_router)
