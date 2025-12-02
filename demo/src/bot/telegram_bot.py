import os
import dotenv
import cv2 as cv
import io
import asyncio
from telegram import Bot

dotenv.load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in the environment variables.")
if not TELEGRAM_GROUP_ID:
    raise ValueError("TELEGRAM_GROUP_ID is not set in the environment variables.")

bot = Bot(TELEGRAM_BOT_TOKEN)

async def alert(img) -> None:
    caption = "Human detected! Please be careful!"
        
    _, img_encoded = cv.imencode('.png', img)  
    img_bytes = img_encoded.tobytes()  

    img_io = io.BytesIO(img_bytes)
    img_io.name = 'alert_image.png'  

    # Send the image via Telegram bot
    await bot.send_photo(chat_id=TELEGRAM_GROUP_ID, photo=img_io, caption=caption)

"""
    # TODO: Just send only message we don't need to create an application
    asyncio.run(alert(frame))

    cap = cv.VideoCapture(0)
    ret, frame = cap.read()
    asyncio.run(alert(frame))
"""

