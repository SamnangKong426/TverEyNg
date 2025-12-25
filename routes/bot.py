from config.db import supabase
from fastapi import APIRouter, HTTPException
from models import BotSchema, BotUpdateSchema

router = APIRouter(prefix="/api/telegram", tags=["telegram"])


# --- CREATE / UPSERT ---
@router.post("/")
async def create_or_update_bot(bot: BotSchema):
    """Creates a new bot config or updates existing one based on user_id"""
    try:
        res = (
            supabase.table("bots")
            .upsert(
                {
                    "user_id": bot.user_id,
                    "bot_token": bot.bot_token,
                    "chat_id": bot.chat_id,
                },
                on_conflict="user_id",
            )
            .execute()
        )
        return {"message": "Success", "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- READ (Single) ---
@router.get("/{user_id}")
async def get_bot(user_id: int):
    """Retrieves the bot config for a specific user"""
    res = supabase.table("bots").select("*").eq("user_id", user_id).execute()
    if not res.data:
        return {}
    return res.data[0]


# --- UPDATE (Partial) ---
@router.patch("/{user_id}")
async def update_bot(user_id: int, bot_update: BotUpdateSchema):
    """Updates specific fields for a user's bot"""
    update_data = {k: v for k, v in bot_update.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided to update")

    res = supabase.table("bots").update(update_data).eq("user_id", user_id).execute()
    return {"message": "Updated", "data": res.data}


# --- DELETE ---
@router.delete("/{user_id}")
async def delete_bot(user_id: int):
    """Removes bot config for a user"""
    supabase.table("bots").delete().eq("user_id", user_id).execute()
    return {"message": "Deleted", "id": user_id}
