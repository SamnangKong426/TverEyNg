from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import httpx

router = APIRouter()

ESP32_STREAM_URL = "http://192.168.1.3"   

@router.get("/")
async def video_feed():

    async def stream_generator():
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", ESP32_STREAM_URL) as stream:
                async for chunk in stream.aiter_bytes():
                    yield chunk

    return StreamingResponse(
        stream_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
