from modes.fixit import handle_fixit_mode
from modes.fridge_scanner import handle_fridge_scan
from modes.kitchen import handle_kitchen_mode, KitchenInput
from modes.home_organizer import handle_home_organizer_mode
from storage.knowledge_loader import KnowledgeLoader

# Load knowledge once
knowledge = KnowledgeLoader().load_all()

class ModeRouter:
    def detect_mode(self, input_text: str) -> str:
        text = input_text.lower()
        if "fix" in text:
            return "Fixit"
        elif "fridge" in text or "scan" in text:
            return "Fridge"
        elif "kitchen" in text or "cook" in text:
            return "Kitchen"
        else:
            return "HomeOrganizer"

    def handle_mode(self, mode: str, input_text: str, user_id: str = "user_123"):
        if mode == "Fixit":
            return handle_fixit_mode(input_text, knowledge=knowledge, user_id=user_id)
        elif mode == "Fridge":
            from fastapi import UploadFile
            from io import BytesIO
            dummy_file = UploadFile(filename="dummy.jpg", file=BytesIO())
            return handle_fridge_scan(dummy_file, knowledge=knowledge, user_id=user_id)
        elif mode == "Kitchen":
            kitchen_input = KitchenInput(
                fridge_items=["milk", "eggs"],
                pantry_items=["rice", "beans"],
                goal="make a healthy dinner",
                user_id=user_id
            )
            return handle_kitchen_mode(kitchen_input, knowledge=knowledge)
        else:
            return handle_home_organizer_mode(input_text, knowledge=knowledge, user_id=user_id)
