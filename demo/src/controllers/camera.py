import cv2 as cv
from src.services import predict

def open_camera():
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        return {"message": "Error: Could not open the camera."}

    while True:
        ret, frame = cap.read()

        if not ret:
            return {"message": "Failed to grab frame, exiting..."}

        results= list(predict(frame))
        annotated_frame = results[0].plot()
        yield results, annotated_frame

    cap.release()
