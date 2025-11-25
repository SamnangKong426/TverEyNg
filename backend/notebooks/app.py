import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse, HTMLResponse

app = FastAPI()

# Store latest frame for each camera
camera_frames = {}

@app.post("/upload-frame")
async def upload_frame(
    camera_id: str = Form(...),
    file: UploadFile = File(...)
):
    data = await file.read()
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

    camera_frames[camera_id] = img
    return {"status": "received"}

def mjpeg_stream(camera_id):
    while True:
        frame = camera_frames.get(camera_id)
        if frame is None:
            continue

        ret, jpeg = cv2.imencode(".jpg", frame)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            jpeg.tobytes() +
            b"\r\n"
        )

@app.get("/camera/{camera_id}")
def camera_feed(camera_id: str):
    return StreamingResponse(
        mjpeg_stream(camera_id),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.get("/dashboard")
def dashboard():
    html = """
    <html>
    <head>
        <title>Multi-Camera Dashboard</title>
        <style>
            body { background: #111; font-family: Arial; }
            .grid { display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                    gap: 10px; }
            .cam { background: black; padding: 5px; }
            img { width: 100%; border-radius: 6px; }
            h2 { color: white; text-align: center; }
        </style>
    </head>
    <body>
        <h2>Live Cameras</h2>
        <div class="grid">
    """

    for cam_id in camera_frames.keys():
        html += f"""
            <div class="cam">
                <img src="/camera/{cam_id}">
                <div style="color:white;text-align:center;">Camera {cam_id}</div>
            </div>
        """

    html += "</div></body></html>"
    return HTMLResponse(html)
