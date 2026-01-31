from fastapi import APIRouter, Form
from lifeos.storage.memory_manager import MemoryManager

class ModeRouter:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/ask", self.ask_handler, methods=["POST"])

    def ask_handler(self, message: str = Form(...), user_id: str = Form(...)):
        mm = MemoryManager(user_id)
        memory = mm.get_all()
        return {
            "summary": f"You said: {message}",
            "user_id": user_id,
            "memory": memory
        }
