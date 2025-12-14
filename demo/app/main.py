import time
import asyncio
import cv2 as cv
import streamlit as st
import services.tracker as tracker
from bot.telegram_bot import alert

st.set_page_config(page_title="TverEyNg", page_icon="👋", layout="wide")

TIMEOUT = 10
LAST_ALERT = 0

# Define the camera sources
cameras = {
    "laptop": 0,  # Local camera (usually webcam)
    "pixel": "https://www.pexels.com/download/video/853889/",
    # "iphone": "http://172.23.5.0:4747/video",  
    # "pixel1": "https://www.pexels.com/download/video/855564/",
    # "pixel2": "https://www.pexels.com/download/video/1776352/",
}


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


async def process_alert(results, annotated_frame):
    """Trigger alert if class 0 is detected and timeout has passed."""
    global LAST_ALERT, TIMEOUT
    now = time.time()

    for r in results:
        if 0 in r.boxes.cls and now - LAST_ALERT >= TIMEOUT:
            await asyncio.create_task(alert(annotated_frame))
            LAST_ALERT = now


# Set the target frame rate to 30 FPS
target_fps = 30
frame_delay = 1 / target_fps  

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

                results, frame = tracker.track(frame)
                await process_alert(results, frame)

                # Update annotated frame
                holders[name].image(frame, caption=name, channels="BGR", width="stretch")
            else:
                pass

        # Sleep to maintain 30 FPS
        # time.sleep(frame_delay)

if __name__ == "__main__":
    asyncio.run(main())
