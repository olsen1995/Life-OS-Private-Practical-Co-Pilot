from __future__ import annotations

from typing import Any, Dict

from lifeos.storage.memory_manager import MemoryManager


def write_memory(user_id: str, memory: Dict[str, Any]) -> Dict[str, Any]:
    mm = MemoryManager(user_id)
    mm.set_all(memory)
    return {"ok": True, "written": len(memory.keys())}


def read_memory(user_id: str) -> Dict[str, Any]:
    mm = MemoryManager(user_id)
    return mm.get_all()


def delete_memory(user_id: str) -> Dict[str, Any]:
    mm = MemoryManager(user_id)

    try:
        import os

        if not os.path.exists(mm.file_path):
            return {"ok": True, "deleted": False}

        os.remove(mm.file_path)
        return {"ok": True, "deleted": True}
    except Exception:
        raise
