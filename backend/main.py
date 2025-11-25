import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from routes import stream_router, camera_router
from routes import camera_router, stream_router
from config.db import create_db_and_tables
from bot.bot import tele_start

app = FastAPI()

# Allow all origins for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

    asyncio.create_task(tele_start())

# Include existing routes
# app.include_router(yolo_router, prefix="/api/yolo")
app.include_router(stream_router, prefix="/api/stream")
app.include_router(camera_router, prefix="/api/cameras")

"""
Run:
uvicorn main:app --host 0.0.0.0 --port 8000
"""
