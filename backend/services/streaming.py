import cv2 as cv
import time
import yolo  # make sure your YOLO model is loaded

ip_cameras = {
    "esp32cam": "http://10.42.0.23/"  # Make sure trailing slash is correct
}

PULL_INTERVAL = 1  # seconds

def capture_frame():
    """ Continuously capture frames from all cameras """
    while True:
        for cam_id, ip in ip_cameras.items():
            cap = cv.VideoCapture(ip)
            ret, frame = cap.read()
            if not ret:
                print(f"[{cam_id}] Failed to capture frame")
                continue
            cap.release()
            yield cam_id, frame
        time.sleep(PULL_INTERVAL)

def stream_frame():
    """ Predict every captured frame and print results """
    for camera_id, frame in capture_frame():
        results = yolo.model.predict(frame, task="detect", conf=0.3, verbose=False)
        print(f"[{camera_id}] Prediction: {results}")

if __name__ == "__main__":
    stream_frame()
