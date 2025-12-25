import os

import requests
from dotenv import load_dotenv

load_dotenv()

URL = str(os.getenv("ULTRALYTICS_PREDICT_URL"))
HEADERS = {"x-api-key": os.getenv("ULTRALYTICS_API_KEY")}
MODEL_URL = os.getenv("ULTRALYTICS_MODEL_URL")


def run_inference(image):
    data = {"model": MODEL_URL, "imgsz": 640, "conf": 0.25, "iou": 0.45}

    with open(image, "rb") as f:
        files = {"file": (os.path.basename(image), f, "image/jpeg")}

        try:
            response = requests.post(
                URL, headers=HEADERS, data=data, files=files, timeout=10
            )

            if response.status_code == 429:
                print("⚠️ Rate limit reached. Skipping this frame.")
                return []

            response.raise_for_status()

            results = response.json().get("images", [{}])[0].get("results", [])

            return [item["class"] for item in results]

        except Exception as e:
            print(f"❌ AI Error: {e}")
            return []


if __name__ == "__main__":
    classes = run_inference("/home/user/Downloads/Telegram Desktop/IMG_1829.JPG")
    print(classes)
