import cv2 as cv
import streamlit as st
from threading import Thread
from queue import Queue
from utils.mocks.ip_cam import ip_cameras  
from app.services.tracker import predict  

st.set_page_config(
    page_title="TverEyNg",
    page_icon="👋",
)

class WorkerThread(Thread):
    def __init__(self, ip_cam, frame_queue):
        super().__init__()
        self.cap = cv.VideoCapture(ip_cam)
        self.frame_queue = frame_queue

        if not self.cap.isOpened():
            st.error(f"Error: Could not open the camera {ip_cam}.")
            return

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                st.warning(f"Failed to grab frame from {self.cap}. Exiting...")
                break

            # Process frame (apply prediction and annotation)
            results = list(predict(frame))
            annotated_frame = results[0].plot()
            self.frame_queue.put(annotated_frame)

        self.cap.release()

frame_queue = Queue()
thread = WorkerThread(ip_cameras["esp32"], frame_queue)
thread.start()

empty_frame = st.empty()

while True:
    if not frame_queue.empty():
        annotated_frame = frame_queue.get()
        empty_frame.image(annotated_frame, channels="RGB")