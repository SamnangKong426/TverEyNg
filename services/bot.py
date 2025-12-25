import os
import tempfile
import time

import requests
from services.ultralytics import run_inference

BOT_URL = "http://127.0.0.1:8001/alert"


def alert(image_src):
    files = {"file": (image_src, open(image_src, "rb"), "image/jpeg")}

    headers = {"accept": "application/json"}

    try:
        response = requests.post(BOT_URL, headers=headers, files=files)
        response.raise_for_status()
        print(response.json())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        files["file"][1].close()


TIMEOUT = 60
LAST_ALERT = 0


def process_alert(image_bytes):
    global LAST_ALERT
    now = time.time()

    if now - LAST_ALERT >= TIMEOUT:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
            temp_file.write(image_bytes)
            temp_path = temp_file.name

        try:
            classes = run_inference(temp_path)

            if 0 in classes:
                alert(temp_path)

            LAST_ALERT = now
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    alert("/home/user/Downloads/Telegram Desktop/IMG_1829.JPG")
