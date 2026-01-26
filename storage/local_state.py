
import os
import json

BASE_PATH = os.path.join(os.path.dirname(__file__), "user_data")

def _get_user_file_path(user_id: str) -> str:
    os.makedirs(BASE_PATH, exist_ok=True)
    return os.path.join(BASE_PATH, f"{user_id}.json")

def get_user_data(user_id: str) -> dict:
    file_path = _get_user_file_path(user_id)
    if not os.path.exists(file_path):
        return {"notes": [], "reminders": [], "tasks": []}
    with open(file_path, "r") as f:
        return json.load(f)

def update_user_data(user_id: str, new_data: dict):
    file_path = _get_user_file_path(user_id)
    data = get_user_data(user_id)
    for key, value in new_data.items():
        if key in data and isinstance(data[key], list):
            data[key].extend(value)
        else:
            data[key] = value
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def clear_user_data(user_id: str):
    file_path = _get_user_file_path(user_id)
    if os.path.exists(file_path):
        os.remove(file_path)
