from typing import Dict, Any

def handle_fixit_mode(input_text: str, knowledge: Dict[str, Any] = {}, user_id: str = "user_123"):
    # Example fixit response
    user_data = knowledge.get(user_id, {})
    fixit_instructions = user_data.get("fixit_instructions", [])
    return {
        "input": input_text,
        "instructions": fixit_instructions or ["No fixit instructions found."]
    }
