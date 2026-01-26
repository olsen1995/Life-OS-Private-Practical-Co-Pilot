
from storage.local_state import get_user_data, update_user_data

def handle_memory_mode(input_text: str, user_id: str = "user_123"):
    input_text = input_text.lower()
    response = {"summary": "", "steps": [], "priority": "normal", "actions": []}

    if "remember" in input_text or "note" in input_text:
        note_content = input_text.replace("remember", "").replace("note", "").strip()
        update_user_data(user_id, {"notes": [note_content]})
        response["summary"] = "Note saved 🧠"
        response["steps"].append(f"I've saved: '{note_content}'")
        response["priority"] = "high"
        response["actions"].append({"type": "note", "payload": {"content": note_content}})

    elif "remind" in input_text or "reminder" in input_text:
        reminder = input_text.replace("remind me", "").replace("reminder", "").strip()
        update_user_data(user_id, {"reminders": [reminder]})
        response["summary"] = "Reminder added ⏰"
        response["steps"].append(f"I'll remind you about: '{reminder}'")
        response["priority"] = "high"
        response["actions"].append({"type": "reminder", "payload": {"content": reminder}})

    elif "show" in input_text or "what" in input_text or "list" in input_text:
        data = get_user_data(user_id)
        response["summary"] = "Here's what I remember:"
        response["steps"].extend([
            f"📝 Notes: {', '.join(data.get('notes', []) or ['None'])}",
            f"⏰ Reminders: {', '.join(data.get('reminders', []) or ['None'])}",
            f"✅ Tasks: {', '.join(data.get('tasks', []) or ['None'])}"
        ])
        response["priority"] = "normal"

    else:
        response["summary"] = "Not sure what memory action to take 🤔"
        response["steps"].append("You can say things like 'remember pick up laundry' or 'show my notes'.")

    return response
