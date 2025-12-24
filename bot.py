import os
import io
import dotenv
from PIL import Image
from telegram import Bot

dotenv.load_dotenv()

TELEGRAM_BOT_TOKEN = str(os.getenv("TELEGRAM_BOT_TOKEN"))
TELEGRAM_GROUP_ID = str(os.getenv("TELEGRAM_GROUP_ID"))

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables.")
if not TELEGRAM_GROUP_ID:
    raise ValueError("TELEGRAM_GROUP_ID is not set in environment variables.")

bot = Bot(TELEGRAM_BOT_TOKEN)


async def send_alert(image: Image.Image) -> None:
    """
    Sends an image to a Telegram group with a warning message.
    """
    caption = "Human detected! Please be careful!"

    # Convert to PNG bytes
    img_io = io.BytesIO()
    image.save(img_io, format="PNG")
    img_io.seek(0)
    img_io.name = "alert_image.png"

    await bot.send_photo(chat_id=TELEGRAM_GROUP_ID, photo=img_io, caption=caption)
