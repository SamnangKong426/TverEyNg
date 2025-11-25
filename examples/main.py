from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import numpy as np
import cv2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = YOLO("yolo11n.pt")
model_ready = True


@app.post("/upload")
async def upload(frame: UploadFile = File(...)):
    if not model_ready:
        return {"success": False, "error": "Model not ready yet"}

    # Read JPEG bytes
    image_bytes = await frame.read()
    image = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # YOLO inference
    results = model.predict(image, conf=0.3, verbose=False)

    # Convert results to JSON-safe format
    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "cls": int(box.cls[0]),
                "conf": float(box.conf[0]),
                "xyxy": box.xyxy[0].tolist()
            })

    return {"success": True, "detections": detections}
