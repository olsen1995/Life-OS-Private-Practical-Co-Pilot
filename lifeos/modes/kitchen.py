from pydantic import BaseModel
from typing import List, Dict, Any

class KitchenInput(BaseModel):
    fridge_items: List[str]
    pantry_items: List[str]
    goal: str
    user_id: str

class KitchenResponse(BaseModel):
    goal: str
    suggestions: List[str]
    fridge_items: List[str]
    pantry_items: List[str]

def handle_kitchen_mode(data: KitchenInput, knowledge: Dict[str, Any] = {}) -> KitchenResponse:
    user_data = knowledge.get(data.user_id, {})
    kitchen_plan = user_data.get("kitchen_plan", {})

    goal = kitchen_plan.get("goal", data.goal)
    suggestions = kitchen_plan.get("suggestions", ["No suggestions available."])

    return KitchenResponse(
        goal=goal,
        suggestions=suggestions,
        fridge_items=data.fridge_items,
        pantry_items=data.pantry_items
    )
