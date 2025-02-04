from settings.constant import get_data
import json
import os


# noinspection PyTypeChecker
def save_data(file_name, block: str | list, new_data):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    data = get_data(file_path)
    if isinstance(block, str):
        data[block] = new_data
    else:
        # Идем по блоку, потом записываем данные
        n = data
        for i in block[:-1]:
            n = n[i]
        n[block[-1]] = new_data
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)
