import io
import os

import cv2 as cv
import dotenv
from telegram import Bot

from .config import load_json

dotenv.load_dotenv()

credentials = load_json("database/credentials.json")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or credentials.get("bot_token")
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID") or credentials.get("group_id")


bot = Bot(str(TELEGRAM_BOT_TOKEN))


async def alert(img) -> None:
    caption = "Human detected! Please be careful!"

    _, img_encoded = cv.imencode(".png", img)
    img_bytes = img_encoded.tobytes()

    img_io = io.BytesIO(img_bytes)
    img_io.name = "alert_image.png"

    # Send the image via Telegram bot
    await bot.send_photo(chat_id=str(TELEGRAM_GROUP_ID), photo=img_io, caption=caption)


"""
    # TODO: Just send only message we don't need to create an application
    asyncio.run(alert(frame))

    cap = cv.VideoCapture(0)
    ret, frame = cap.read()
    asyncio.run(alert(frame))
"""
