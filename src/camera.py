import cv2 as cv
import streamlit as st


@st.cache_resource
def start_camera(ip):
    cam = cv.VideoCapture(ip)
    if not cam.isOpened():
        raise RuntimeError("Could not open webcam")
    return cam
