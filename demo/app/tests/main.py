import os
import time
import json
import asyncio
import threading
import cv2 as cv
import streamlit as st
from ultralytics import YOLO
from bot.telegram_bot import alert

st.set_page_config(page_title="TverEyNg", page_icon="👋", layout="wide")


# ==============================================================================

FILE_PATH = "database/data.json"


def save_json(data, filename="database/data.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_json(filename="database/data.json"):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data


cameras = load_json()


# ==============================================================================
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
        classes=[0],
    )
    results = list(results)
    return results


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
            cv.putText(
                frame, label, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.6, color, 2
            )

    return frame


def track_frame(name, frame, results_holder):
    """Run tracking in a separate thread."""
    results = track(frame)
    results_holder[name] = results


# ==============================================================================


def play_sound(sound_path):
    def play():
        os.system("mpg123 " + sound_path)

    sound_thread = threading.Thread(target=play)
    sound_thread.start()


# ==============================================================================

TIMEOUT = 30
LAST_ALERT = 0


def process_alert(results, annotated_frame):
    """Trigger alert if class 0 is detected and timeout has passed."""
    global LAST_ALERT, TIMEOUT
    now = time.time()

    for r in results:
        if 0 in r.boxes.cls and now - LAST_ALERT >= TIMEOUT:
            play_sound("assets/thief_sound.mp3")
            alert_thread = threading.Thread(
                target=lambda: asyncio.run(alert(annotated_frame))
            )
            alert_thread.start()
            LAST_ALERT = now


# ==============================================================================


def set_config():
    @st.dialog("Add your camera")
    def add_camera():
        name = st.text_input("Camera Name")
        ip = st.text_input("IP Camera Address:")

        if st.button("Submit"):
            cameras[name] = ip
            save_json(cameras, FILE_PATH)
            st.rerun()

    @st.dialog("Delete camera")
    def delete_camera():
        if not cameras:
            st.warning("No cameras to delete")
            return

        camera_to_delete = st.selectbox("Select camera", list(cameras.keys()))

        if st.button("Delete"):
            del cameras[camera_to_delete]
            save_json(cameras, FILE_PATH)
            st.success(f"Deleted {camera_to_delete}")
            st.session_state.clear() # Clear all session state
            st.cache_data.clear() # Clear all cached data
            st.rerun() # Rerun the entire script

    @st.dialog("Telegram")
    def set_telegram():
        bot_token = st.text_input("Bot Token: ")
        group_id = st.text_input("Group ID: ")

        if st.button("Submit"):
            cameras["telegram"] = {"bot_token": bot_token, "group_id": group_id}
            save_json(cameras, FILE_PATH)
            st.rerun()



    cols = st.columns(2, vertical_alignment="bottom")

    with cols[0]:
        st.title("👋 TverEyNg")

    with cols[1]:
        with st.container(horizontal=True, horizontal_alignment="right"):
            if st.button("Telegram"):
                set_telegram()

            if st.button("Add Camera"):
                add_camera()

            if st.button("Delete Camera"):
                delete_camera()


set_config()

# ==============================================================================


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


# ==============================================================================


def main():
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
                process_alert(results, frame)

                # Update annotated frame
                holders[name].image(
                    frame, caption=name, channels="BGR", width="stretch"
                )
            else:
                pass

        # Sleep to maintain 30 FPS
        time.sleep(1 / 30)


main()
