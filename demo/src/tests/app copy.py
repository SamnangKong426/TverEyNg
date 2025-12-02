from unittest import result
import cv2 as cv
import streamlit as st
from utils.mocks.ip_cam import ip_cameras
from services.track_obj import predict

st.set_page_config(
    page_title="TverEyNg",
    page_icon="👋",
)

# for idx, (camera_name, ip_cam) in enumerate(ip_cameras.items()):
#     st.image(ip_cam, caption=str(camera_name), width="stretch", output_format="auto", channels="RGB")

cap = cv.VideoCapture(str(ip_cameras["iphone"]))

if not cap.isOpened():
    st.error("Error: Could not open the camera.")

det_frame = st.empty()

while True:
    ret, frame = cap.read()

    if not ret:
        st.warning("Failed to grab frame, exiting...")
        break  

    results= list(predict(frame))
    annotated_frame = results[0].plot()
    det_frame.image(annotated_frame, caption="Processed Frame", width="stretch", channels="BGR")