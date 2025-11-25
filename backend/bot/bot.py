import os
import dotenv
import asyncio

from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

dotenv.load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")

bot = Bot(TELEGRAM_BOT_TOKEN)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')
    await alert()

async def alert() -> None:
    caption = "Human detected! Please be careful!"
    await bot.send_photo(TELEGRAM_GROUP_ID, open('bot/image.png', 'rb'), caption=caption)


app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("hello", hello))

async def tele_start():
    try:
        await app.initialize()
        await app.start()
        await app.updater.start_polling()  
        # keep running
        await asyncio.Future()  # run forever
    finally:
        await bot.shutdown()

"""
Call this example Telegram bot will be ready

Example: 
    asyncio.create_task(tele_start())
"""