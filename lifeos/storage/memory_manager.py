class MemoryManager:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def get_all(self) -> dict:
        return {
            "status": "stub",
            "user_id": self.user_id,
            "memory_items": ["demo1", "demo2"]
        }
