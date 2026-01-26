
from modes.fixit import handle_fixit_mode
from modes.fridge_scanner import handle_fridge_scan
from modes.kitchen import handle_kitchen_mode, KitchenInput
from modes.home_organizer import handle_home_organizer_mode
from modes.memory import handle_memory_mode
from storage.knowledge_loader import KnowledgeLoader

# Load knowledge once for all modes
knowledge = KnowledgeLoader().load_all()

class ModeRouter:
    def __init__(self):
        self.mode_keywords = {
            "Fixit": ["fix", "repair", "broken", "tool"],
            "Fridge": ["fridge", "scan", "grocery", "inventory"],
            "Kitchen": ["cook", "recipe", "kitchen", "meal"],
            "HomeOrganizer": ["organize", "sort", "declutter", "clean"],
            "Memory": ["remember", "note", "remind", "recall", "what did", "show"]
        }

    def route_request(self, input_text: str) -> str:
        text = input_text.lower()
        for mode, keywords in self.mode_keywords.items():
            if any(word in text for word in keywords):
                return mode
        return "Fallback"

    def handle_mode(self, mode: str, input_text: str, user_id: str = "user_123"):
        if mode == "Fixit":
            return handle_fixit_mode(input_text, knowledge=knowledge, user_id=user_id)
        elif mode == "Fridge":
            return handle_fridge_scan(input_text, knowledge=knowledge, user_id=user_id)
        elif mode == "Kitchen":
            return handle_kitchen_mode(input_text, knowledge=knowledge, user_id=user_id)
        elif mode == "HomeOrganizer":
            return handle_home_organizer_mode(input_text, knowledge=knowledge, user_id=user_id)
        elif mode == "Memory":
            return handle_memory_mode(input_text, user_id=user_id)
            return handle_home_organizer_mode(input_text, knowledge=knowledge, user_id=user_id)
        else:
            return {
                "summary": "I'm not quite sure what you meant 🤔",
                "steps": ["Try rephrasing your request.", "You can say things like 'fix the sink' or 'what can I cook?'"],
                "priority": "low",
                "actions": []
            }
