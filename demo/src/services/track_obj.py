from ultralytics import YOLO

model = YOLO("src/models/yolo11n.onnx")

def predict(frame):
    results = model.track(frame, conf=0.5, verbose=False, stream=True)
    return results
