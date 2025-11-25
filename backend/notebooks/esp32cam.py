import cv2
from ultralytics import YOLO

# Set the URL for the video stream
url = "http://10.42.0.23:80/"  

# Load the YOLO model from the ONNX file
model = YOLO("/home/user/Documents/TverEyNg/backend/models/yolo11n.onnx")

# Open the video stream
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Cannot open stream")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # Run object detection on the current frame
    results = model(frame, conf=0.3, iou=0.5)  # Use predict() for detection on a single frame

    # Draw results on the frame
    frame_with_results = results[0].plot()  # Plot detection results on the frame

    # Display the frame with detections
    cv2.imshow("YOLO Detection", frame_with_results)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()
