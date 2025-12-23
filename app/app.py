import time

import cv2 as cv
import streamlit as st

from src.alerts import process_alert
from src.camera import start_camera
from src.config import set_config
from src.detection import track
from src.utils import load_json

st.set_page_config(page_title="TverEyNg", page_icon="👋", layout="wide")

if "is_setting" not in st.session_state:
    st.session_state.is_setting = 0

cameras = load_json()
set_config()

cameras_objects = {name: start_camera(ip) for name, ip in cameras.items()}
cols = st.columns(2, gap="medium", vertical_alignment="top", width="stretch")
holders = {}

NO_CONNECTION_IMAGE = "assets/no_connected.png"
for idx, (name, cam) in enumerate(cameras_objects.items()):
    placeholder = cols[idx % 2].image(
        NO_CONNECTION_IMAGE,
        channels="BGR",
        width="stretch",
    )
    holders[name] = placeholder


def main():
    while True:
        if st.session_state.is_setting == 1:
            break
        for name, cam in cameras_objects.items():
            ret, frame = cam.read()
            if not ret:
                cam.set(cv.CAP_PROP_POS_FRAMES, 0)
                continue
            frame = cv.resize(frame, (640, 480))
            results, frame = track(frame)
            process_alert(results, frame)
            holders[name].image(frame, caption=name, channels="BGR", width="stretch")

main()
