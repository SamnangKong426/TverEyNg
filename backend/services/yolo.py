from ultralytics import YOLO


model = YOLO("models/yolo11n.onnx")

"""
Input image in order to get predicted result

Example:
    results = model.predict(image, conf=0.3, verbose=False)
"""