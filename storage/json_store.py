import json
from pathlib import Path
from typing import Any, Dict

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def _user_file(user_id: str) -> Path:
    return DATA_DIR / f"{user_id}.json"


def load_user_data(user_id: str) -> Dict[str, Any]:
    file_path = _user_file(user_id)

    if not file_path.exists():
        return {}

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_user_data(user_id: str, data: Dict[str, Any]) -> None:
    file_path = _user_file(user_id)

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
