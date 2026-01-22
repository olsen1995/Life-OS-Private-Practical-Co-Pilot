import re

class ModeRouter:
    def __init__(self):
        self.modes = {
            "DayPlanner": [
                "plan", "schedule", "calendar", "agenda", "itinerary", "organize", "mapped out"
            ],
            "LifeCoach": [
                "overwhelmed", "burnout", "unmotivated", "purpose", "stuck", "clarity",
                "self-sabotage", "focus", "mental", "motivation"
            ],
            "FixIt": [
                "broken", "fix", "repair", "leaking", "cracked", "wobbling", "not working",
                "malfunction", "jammed", "won’t start", "problem", "issue"
            ],
            "Device Optimization": [
                "slow", "optimize", "speed up", "performance", "battery", "startup apps",
                "cache", "lag", "storage", "overheating"
            ],
            "Kitchen": [
                "meal", "cook", "recipe", "food", "kitchen", "fridge", "grocery", "dinner", "breakfast"
            ]
        }

    def detect_mode(self, user_input: str) -> str:
        user_input = user_input.lower()
        matched_modes: dict[str, int] = {}

        for mode, keywords in self.modes.items():
            for keyword in keywords:
                if keyword in user_input:
                    matched_modes[mode] = matched_modes.get(mode, 0) + 1

        if matched_modes:
            return max(matched_modes, key=lambda k: matched_modes[k])
        return "Unknown"
