from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com", api_key="gLjKEn17mDrNWJde9jCi"
)


def inference(image_src):
    result = CLIENT.infer(image_src, model_id="human-detection-dmwvg/1")
    return result


if __name__ == "__main__":
    result = inference("/home/user/Downloads/Telegram Desktop/IMG_1827.JPG")
    print(result)
