import json
from pathlib import Path


class MemoryManager:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.base_path = Path("storage/user_memory")
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.file_path = self.base_path / f"{user_id}.json"

    def get_all(self):
        if not self.file_path.exists():
            return {}
        return json.loads(self.file_path.read_text(encoding="utf-8"))

    def set_all(self, memory: dict) -> None:
        if memory is None:
            memory = {}
        self.file_path.write_text(
            json.dumps(memory, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def clear(self):
        if self.file_path.exists():
            self.file_path.unlink()
