
import re
from openai import OpenAI
from storage.knowledge_loader import KnowledgeLoader
from modes.fixit import handle_fixit_mode
from modes.fridge_scanner import handle_fridge_scan
from modes.kitchen import handle_kitchen_mode
from modes.home_organizer import handle_home_organizer_mode
from modes.memory import handle_memory_mode

# Load shared knowledge
knowledge = KnowledgeLoader().load_all()

class ModeRouter:
    def __init__(self, openai_client: OpenAI):
        self.client = openai_client

    def route_request(self, input_text: str) -> str:
        """Use GPT to detect the best mode based on user input."""
        try:
            system_prompt = (
                "You are a mode classifier for an AI assistant. "
                "Decide the BEST matching mode from the following list, based on the input:
"
                "- Fixit
- Fridge
- Kitchen
- HomeOrganizer
- Memory
"
                "Respond ONLY with the mode name. No punctuation or explanation.

"
                f"User input: {input_text}
Answer:"
            )
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": system_prompt}],
                max_tokens=10,
                temperature=0.0
            )
            mode = response.choices[0].message.content.strip()
            if mode not in ["Fixit", "Fridge", "Kitchen", "HomeOrganizer", "Memory"]:
                return "Fallback"
            return mode
        except Exception as e:
            print(f"[Router Error] {e}")
            return "Fallback"

    def handle_mode(self, mode: str, input_text: str, user_id: str = "user_123"):
        """Call the corresponding handler based on mode."""
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
        else:
            return {
                "summary": "I’m not quite sure what you meant 🤔",
                "steps": ["Try rephrasing your request.", "Examples: 'fix sink', 'what can I cook?', 'remember this'"],
                "priority": "low",
                "actions": []
            }
