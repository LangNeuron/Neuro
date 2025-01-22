import json
import os


if os.path.exists(r"settings/settings.json"):
    with open(r"settings/settings.json", "r") as file:
        data = json.load(file)
else:
    exit(1)
