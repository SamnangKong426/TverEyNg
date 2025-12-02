import cv2 as cv

def capture_frame(ip_cam):
    cap = cv.VideoCapture(ip_cam)
    
    if not cap.isOpened():
        print("Error: Could not open video stream.")

    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")

    cap.release()
    
    return frame
