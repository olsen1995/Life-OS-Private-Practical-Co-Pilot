from modes.fixit import handle_fixit_mode
from modes.fridge_scanner import handle_fridge_scan
from modes.kitchen import handle_kitchen_mode, KitchenInput
from modes.home_organizer import handle_home_organizer_mode


def get_mode(input_text: str) -> str:
    input_text_lower = input_text.lower()

    if "fix" in input_text_lower:
        return "Fixit"
    elif "fridge" in input_text_lower or "scan" in input_text_lower:
        return "Fridge"
    elif "kitchen" in input_text_lower or "cook" in input_text_lower:
        return "Kitchen"
    else:
        return "HomeOrganizer"


class ModeRouter:
    def handle_mode(self, mode: str, input_text: str):
        if mode == "Fixit":
            return handle_fixit_mode(input_text)

        elif mode == "Fridge":
            # Placeholder UploadFile until real file upload is wired
            from fastapi import UploadFile
            from io import BytesIO

            dummy_file = UploadFile(
                filename="dummy.jpg",
                file=BytesIO()
            )

            return handle_fridge_scan(dummy_file)

        elif mode == "Kitchen":
            # ✅ FIX: fridge_items and pantry_items MUST be List[str]

            kitchen_input = KitchenInput(
                fridge_items=["milk", "eggs"],
                pantry_items=["rice", "beans"],
                goal="make a healthy dinner",
                user_id="user_123"
            )

            return handle_kitchen_mode(kitchen_input)

        else:
            return handle_home_organizer_mode(input_text)
