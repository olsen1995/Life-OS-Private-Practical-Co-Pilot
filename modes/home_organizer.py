from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def handle_home_organizer_mode(user_input: str):
    prompt = f"""
You are a professional home organization assistant.

User request: {user_input}

Return a step-by-step plan with clear sections.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You help organize homes efficiently."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        content = response.choices[0].message.content
        return {"plan": content.strip() if content else "No response from model."}

    except Exception as e:
        return {"error": str(e)}
