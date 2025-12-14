import os
import time
import asyncio
import threading
import cv2 as cv
import streamlit as st
from ultralytics import YOLO
from bot.telegram_bot import alert

st.set_page_config(page_title="TverEyNg", page_icon="👋", layout="wide")

TIMEOUT = 30
LAST_ALERT = 0

# Define the camera sources
cameras = {
    "laptop": 0,  # Local camera (usually webcam)
    "pixel": "https://www.pexels.com/download/video/853889/",
    # "iphone": "http://172.23.5.0:4747/video",
    # "pixel1": "https://www.pexels.com/download/video/855564/",
    # "pixel2": "https://www.pexels.com/download/video/1776352/",
}


model = YOLO("models/yolo11n.pt")
model.to("cpu")


def track(frame):
    results = model.predict(
        frame,
        conf=0.5,
        imgsz=640,
        max_det=1,
        stream=True,
        verbose=False,
        stream_buffer=True,
        vid_stride=1000,
        classes=[0]
    )
    results = list(results)
    return results



@st.cache_resource
def start_camera(ip=0):
    cam = cv.VideoCapture(ip)
    if not cam.isOpened():
        raise RuntimeError("Could not open webcam")
    return cam


cameras_objects = {}
for name, ip in cameras.items():
    cameras_objects[name] = start_camera(ip)

cols = st.columns(2, gap="medium", vertical_alignment="top", width="stretch")

holders = {}

for idx, (name, cam) in enumerate(cameras_objects.items()):
    if idx % 2 == 0:
        with cols[0]:
            holders[name] = st.image(
                "https://cdn.osxdaily.com/wp-content/uploads/2013/12/there-is-no-connected-camera-mac.jpg",
                channels="BGR",
                width="stretch",
            )
    else:
        with cols[1]:
            holders[name] = st.image(
                "https://cdn.osxdaily.com/wp-content/uploads/2013/12/there-is-no-connected-camera-mac.jpg",
                channels="BGR",
                width="stretch",
            )
def draw_bounding_boxes(frame, results):
    """Draw bounding boxes on the frame using OpenCV"""
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy() 
        confidences = result.boxes.conf.cpu().numpy()  
        class_ids = result.boxes.cls.cpu().numpy() 
        
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box.astype(int)
            confidence = confidences[i]
            class_id = int(class_ids[i])

            color = (0, 255, 0) 

            cv.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            label = f"Class {class_id}: {confidence:.2f}"
            cv.putText(frame, label, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    return frame



def track_frame(name, frame, results_holder):
    """Run tracking in a separate thread."""
    results = track(frame)
    results_holder[name] = (results)


def play_sound(sound_path):
    def play():
        os.system("mpg123 " + sound_path)

    sound_thread = threading.Thread(target=play)
    sound_thread.start()


async def process_alert(results, annotated_frame):
    """Trigger alert if class 0 is detected and timeout has passed."""
    global LAST_ALERT, TIMEOUT
    now = time.time()

    for r in results:
        if 0 in r.boxes.cls and now - LAST_ALERT >= TIMEOUT:
            play_sound("assets/thief_sound.mp3")
            await asyncio.create_task(alert(annotated_frame))
            LAST_ALERT = now


async def main():
    while True:
        for idx, (name, cam) in enumerate(cameras_objects.items()):
            ret, frame = cam.read()

            if not ret:
                # Reset to the beginning
                cam.set(cv.CAP_PROP_POS_FRAMES, 0)
                continue

            if ret:
                frame = cv.resize(frame, (640, 480))

                results = track(frame)

                frame = draw_bounding_boxes(frame, results)
                await process_alert(results, frame)

                # Update annotated frame
                holders[name].image(
                    frame, caption=name, channels="BGR", width="stretch"
                )
            else:
                pass

        # Sleep to maintain 30 FPS
        time.sleep(1 / 30)


if __name__ == "__main__":
    asyncio.run(main())
