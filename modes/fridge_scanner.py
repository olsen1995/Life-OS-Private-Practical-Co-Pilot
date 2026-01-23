from PIL import Image
import pytesseract
from fastapi import UploadFile
from typing import List, Dict, Any

class FridgeScanResult:
    def __init__(self, ingredients=None, recipes=None):
        self.ingredients = ingredients or []
        self.recipes = recipes or []

def handle_fridge_scan(file: UploadFile, knowledge: dict, user_id: str) -> FridgeScanResult:
    contents = file.file.read()
    try:
        image = Image.open(file.file)
        text = pytesseract.image_to_string(image)
        ingredients = [line.strip() for line in text.split("\n") if line.strip()]
    except:
        ingredients = []

    # Use knowledge for user-specific recipes
    user_data = knowledge.get(user_id, {})
    recipes = user_data.get("recipes", [])

    return FridgeScanResult(ingredients=ingredients, recipes=recipes)
