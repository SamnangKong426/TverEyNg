import streamlit as st
import cv2 as cv
import time

st.set_page_config(page_title="TverEyNg", page_icon="👋")

@st.cache_resource # Use for multiple user
def start_camera():
    cam = cv.VideoCapture(0)
    if not cam.isOpened():
        raise RuntimeError("Could not open webcam")
    return cam

camera = start_camera()
holder = st.empty()

while 1:
    ret, frame = camera.read()
    if ret:
        holder.image(frame, channels="BGR")
    else:
        st.write("Failed to capture frame.")
    time.sleep(0.05)
