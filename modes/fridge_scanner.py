from PIL import Image
from fastapi import UploadFile
from typing import Dict, Any

class FridgeScanResult:
    def __init__(self, ingredients=None, recipes=None):
        self.ingredients = ingredients or []
        self.recipes = recipes or []

def handle_fridge_scan(file: UploadFile, knowledge: Dict[str, Any] = {}, user_id: str = "user_123") -> FridgeScanResult:
    contents = file.file.read()
    try:
        image = Image.open(file.file)
        import pytesseract
        text = pytesseract.image_to_string(image)
        ingredients = [line.strip() for line in text.split("\n") if line.strip()]
    except:
        ingredients = []

    user_data = knowledge.get(user_id, {})
    recipes = user_data.get("recipes", [])

    return FridgeScanResult(ingredients=ingredients, recipes=recipes)
