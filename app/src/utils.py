import json

FILE_PATH = "database/data.json"


def save_json(data, filename=FILE_PATH):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_json(filename=FILE_PATH):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)
