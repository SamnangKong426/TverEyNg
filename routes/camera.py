import asyncio
import time

from config.db import supabase
from fastapi import (
    APIRouter,
    BackgroundTasks,
    HTTPException,
    Request,
)
from fastapi.responses import StreamingResponse
from models import CameraSchema
from services.bot import process_alert

router = APIRouter(prefix="/api/cameras", tags=["camera"])


# CREATE: Register a new camera
@router.post("/")
async def add_camera(camera: CameraSchema):
    try:
        response = (
            supabase.table("cameras")
            .insert({"name": camera.name, "ip": camera.ip, "user_id": camera.user_id})
            .execute()
        )

        return {"status": "success", "data": response.data}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")


@router.get("/")
async def get_cameras(user_id: str):
    response = supabase.table("cameras").select("*").eq("user_id", user_id).execute()

    return response.data


# UPDATE: Update IP or Name by ID
@router.put("/{camera_id}")
async def update_camera(camera_id: int, camera: CameraSchema):
    data, count = (
        supabase.table("cameras")
        .update({"name": camera.name, "ip": camera.ip})
        .eq("id", camera_id)
        .execute()
    )

    if not data[1]:
        raise HTTPException(status_code=404, detail="Camera not found")
    return {"status": "updated", "data": data[1]}


# DELETE: Remove a camera
@router.delete("/{camera_id}")
async def delete_camera(camera_id: int):
    data, count = supabase.table("cameras").delete().eq("id", camera_id).execute()
    return {"status": "deleted"}


latest_frames = {}


LAST_ALERT_TIMES = {}
ALERT_COOLDOWN = 10  # Seconds to wait between alerts


@router.post("/upload/{camera_id}")
async def upload_image(
    camera_id: str, request: Request, background_tasks: BackgroundTasks
):
    global LAST_ALERT_TIME
    image_bytes = await request.body()

    current_time = time.time()

    latest_frames[camera_id] = {"bytes": image_bytes, "timestamp": current_time}
    last_time = LAST_ALERT_TIMES.get(camera_id, 0)

    if current_time - last_time > ALERT_COOLDOWN:
        background_tasks.add_task(process_alert, image_bytes)
        LAST_ALERT_TIMES[camera_id] = current_time

    return {"status": "success"}


@router.get("/video_feed/{camera_id}")
async def video_feed(camera_id: str):
    """
    Returns a multipart stream that Streamlit or a browser can display.
    """
    if camera_id not in latest_frames:
        pass

    return StreamingResponse(
        gen_frames(camera_id), media_type="multipart/x-mixed-replace; boundary=frame"
    )


async def gen_frames(camera_id: str):
    """
    Generator that constantly yields the latest frame for the multipart stream.
    """
    while True:
        if camera_id in latest_frames:
            frame = latest_frames[camera_id]["bytes"]
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
        else:
            await asyncio.sleep(0.5)
            continue

        await asyncio.sleep(0.05)
