import os
from ultralytics import YOLO

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
        classes=[0]
    )
    results = list(results)
    frame_ = results[0].plot()
    return results, frame_
