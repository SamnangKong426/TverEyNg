import time
import requests
import cv2 as cv
import streamlit as st
from src.camera import start_camera
from src.config import set_config

BASE_URL = st.secrets["server"]["server_url"]

@st.cache_resource
def get_user_cameras(user_id):
    try:
        res = requests.get(f"{BASE_URL}/cameras/", params={"user_id": user_id})
        res.raise_for_status()
        camera_data = res.json()

        init_cameras = {}
        for c in camera_data:
            feed_url = f"{BASE_URL}/cameras/video_feed/{c['id']}"
            cap = start_camera(feed_url)
            if cap:
                init_cameras[c["name"]] = cap
        return init_cameras
    except Exception as e:
        st.error(f"Error loading cameras: {e}")
        return {}

def dashboard():
    st.set_page_config(page_title="TverEyNg", page_icon="👋", layout="wide")
    set_config()

    if "is_setting" not in st.session_state:
        st.session_state.is_setting = 0

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please log in to view your cameras.")
        return

    cameras_objects = get_user_cameras(user_id)

    if not cameras_objects:
        st.info("No cameras found for your account.")
        return

    cols = st.columns(2, gap="medium")
    holders = {}
    for idx, name in enumerate(cameras_objects.keys()):
        holders[name] = cols[idx % 2].empty() 

    while st.session_state.is_setting == 0:
        for name, cam in cameras_objects.items():
            ret, frame = cam.read()
            if ret:
                frame = cv.resize(frame, (640, 480))
                holders[name].image(
                    frame, caption=name, channels="BGR", width='stretch'
                )
            else:
                continue

        time.sleep(0.05)