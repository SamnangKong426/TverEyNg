import streamlit as st
import cv2 as cv
import time

st.set_page_config(page_title="TverEyNg", page_icon="👋", layout="wide")

# Define the camera sources
cameras = {
    # "laptop": 0,  # Local camera (usually webcam)
    # "iphone": "http://172.23.5.0:4747/video",  # IP camera URL (check your URL format)
    "pixel": "https://www.pexels.com/download/video/853889/",
    "pixel1": "https://www.pexels.com/download/video/855564/",
    "pixel2": "https://www.pexels.com/download/video/1776352/",
    "pixel3": "https://www.pexels.com/download/video/1776352/"

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

# Set the target frame rate to 30 FPS
target_fps = 30
frame_delay = 1 / target_fps  # Delay between frames for 30 FPS

cols = st.columns(2, gap="medium", vertical_alignment="top", width="stretch")

holders = {}

for idx, (name, cam) in enumerate(cameras_objects.items()):
    if idx % 2 == 0:
        with cols[0]:
            holders[name] = st.image("https://cdn.osxdaily.com/wp-content/uploads/2013/12/there-is-no-connected-camera-mac.jpg", channels="BGR", width="stretch")
    else:
        with cols[1]:
            holders[name] = st.image("https://cdn.osxdaily.com/wp-content/uploads/2013/12/there-is-no-connected-camera-mac.jpg", channels="BGR", width="stretch")
        
# Display video feed in each column
while 1:
    for idx, (name, cam) in enumerate(cameras_objects.items()):
        ret, frame = cam.read()
        if ret:
            frame = cv.resize(frame, (640, 480))
            holders[name].image(frame, channels="BGR", width="stretch")
        else:
            pass

        # Sleep to maintain 30 FPS
    time.sleep(frame_delay)
