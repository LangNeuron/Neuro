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
        if len(block) == 1:
            data[block[0]] = new_data
        elif len(block) == 2:
            data[block[0]][block[1]] = new_data
        elif len(block) == 3:
            data[block[0]][block[1]][block[2]] = new_data
        elif len(block) == 4:
            data[block[0]][block[1]][block[2]][block[3]] = new_data
        elif len(block) == 5:
            data[block[0]][block[1]][block[2]][block[3]][block[4]] = new_data
        else:
            print("Нужен еще блок settings//save_data")
            exit(1)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)
