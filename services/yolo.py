import requests

URL = "https://sudomlninja-tvereyngyolo.hf.space/upload"


def run_inference(image_path):
    with open(image_path, "rb") as f:
        files = {"frame": (image_path, f, "image/jpeg")}
        headers = {"accept": "application/json"}

        try:
            response = requests.post(URL, headers=headers, files=files)
            response.raise_for_status()

            data = response.json()

            if "detections" in data:
                return [obj["cls"] for obj in data["detections"]]
            return []

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


if __name__ == "__main__":
    result = run_inference("/home/user/Downloads/Telegram Desktop/IMG_1829.JPG")
    print(result)
