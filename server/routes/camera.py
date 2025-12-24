from fastapi import APIRouter, HTTPException

from config.db import supabase
from models import CameraSchema

router = APIRouter(prefix="/camera", tags=["camera"])


# CREATE: Register a new camera
@router.post("/")
async def create_camera(camera: CameraSchema):
    data, count = (
        supabase.table("cameras")
        .insert({"name": camera.name, "ip": camera.ip})
        .execute()
    )
    return {"status": "success", "data": data[0]}


# READ: Get all registered cameras
@router.get("/")
async def get_cameras():
    response = supabase.table("cameras").select("*").execute()
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
