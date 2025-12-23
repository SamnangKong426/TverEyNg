import cv2 as cv
from ultralytics import YOLO

model = YOLO("models/last.pt")
model.to("cpu")


def track(frame):
    results = model.track(
        frame,
        conf=0.3,
        iou=0.5,
        verbose=False
    )

    # Visualize the results on the frame
    annotated_frame = results[0].plot()
    return list(results), annotated_frame


def draw_bounding_boxes(frame, results):
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy()

        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box.astype(int)
            confidence = confidences[i]
            class_id = int(class_ids[i])

            color = (0, 255, 0)
            cv.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            label = f"Class {class_id}: human ({confidence:.2f})"
            cv.putText(
                frame, label, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.6, color, 2
            )
    return frame
