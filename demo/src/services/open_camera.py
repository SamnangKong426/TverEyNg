import cv2 as cv

def open_camera(camera_id=0):
    cap = cv.VideoCapture(camera_id)
    if not cap.isOpened():
        raise RuntimeError("Camera could not be opened")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        yield frame  # send frame to Streamlit

    cap.release()
