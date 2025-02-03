import json
import os


def get_data(file_name: str = "settings.json"):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data
