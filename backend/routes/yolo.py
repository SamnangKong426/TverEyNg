from fastapi import APIRouter, WebSocket
from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2 as cv

from services.yolo import model

router = APIRouter()

@router.post("/upload")
async def upload(frame: UploadFile = File(...)):

    # Read JPEG bytes
    image_bytes = await frame.read()
    image = np.frombuffer(image_bytes, np.uint8)
    image = cv.imdecode(image, cv.IMREAD_COLOR)

    # YOLO inference
    results = model.predict(image, conf=0.3, verbose=False)

    # Convert to JSON format
    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "cls": int(box.cls[0]),
                "conf": float(box.conf[0]),
                "xyxy": box.xyxy[0].tolist()
            })

    return {"success": True, "detections": detections}

"""
Just add the below code to your main FastAPI app

Example:
    app.include_router(router)
"""