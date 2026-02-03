import json
from pathlib import Path
from typing import Any, Dict


class MemoryManager:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.base_path = Path("storage/user_memory")
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.file_path = self.base_path / f"{user_id}.json"

    def get_all(self) -> Dict[str, Any]:
        if not self.file_path.exists():
            return {}
        return json.loads(self.file_path.read_text(encoding="utf-8"))

    def set_all(self, memory: Dict[str, Any]) -> None:
        """
        Replace the user's memory object with the provided dict.
        This is the write-path used by POST /memory in ModeRouter.
        """
        if memory is None:
            memory = {}
        if not isinstance(memory, dict):
            raise ValueError("memory must be a dict")

        self.file_path.write_text(
            json.dumps(memory, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def clear(self) -> None:
        if self.file_path.exists():
            self.file_path.unlink()
