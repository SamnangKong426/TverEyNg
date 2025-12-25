import time

import cv2
import requests

CAMERA_ID = "1"
SERVER_URL = f"https://tvereyngserver.onrender.com/api/cameras/upload/{CAMERA_ID}"


def start_webcam_stream():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print(f"Streaming to {SERVER_URL}... Press 'q' to stop.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        _, img_encoded = cv2.imencode(".jpg", frame)
        image_bytes = img_encoded.tobytes()

        try:
            requests.post(
                SERVER_URL,
                data=image_bytes,
                headers={"Content-Type": "application/octet-stream"},
            )
        except Exception as e:
            print(f"Error sending frame: {e}")

        time.sleep(0.1)

        # cv2.imshow('Webcam Simulator', frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_webcam_stream()
