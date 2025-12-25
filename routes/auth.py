from config.db import supabase
from fastapi import APIRouter

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/sync")
async def sync_user(user: dict):
    res = supabase.table("users").select("id").eq("email", user["email"]).execute()

    if res.data:
        return {"user_id": res.data[0]["id"]}
    else:
        new_user = (
            supabase.table("users")
            .insert({"email": user["email"], "name": user["name"]})
            .execute()
        )
        return {"user_id": new_user.data[0]["id"]}
