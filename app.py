import io

from fastapi import FastAPI, File, UploadFile
from PIL import Image

from bot import send_alert

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello! welcome to Telegram Bot Microservice"}


@app.post("/alert")
async def alert_endpoint(file: UploadFile = File(...)):
    """
    Receive an image and send a Telegram alert.
    """
    image_bytes = await file.read()

    try:
        image = Image.open(io.BytesIO(image_bytes))
    except Exception:
        return {"status": "error", "message": "Invalid image file"}

    await send_alert(image)
    return {"status": "success", "message": "Alert sent"}
