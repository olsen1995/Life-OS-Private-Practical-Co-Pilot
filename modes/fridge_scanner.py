from fastapi import UploadFile
from openai import OpenAI
from PIL import Image
import pytesseract
import io
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def handle_fridge_scan(file: UploadFile):
    contents = file.file.read()
    image = Image.open(io.BytesIO(contents))

    # OCR with pytesseract
    text = pytesseract.image_to_string(image)

    # Ask GPT to interpret the text as ingredients
    prompt = f"Given the following text extracted from a fridge scan image, identify the list of ingredients or items:\n\n{text}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # publicly accessible + vision capable
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    message = response.choices[0].message
    ingredients = message.content.strip() if message and message.content else "Could not extract ingredients."

    return {"extracted_ingredients": ingredients}
