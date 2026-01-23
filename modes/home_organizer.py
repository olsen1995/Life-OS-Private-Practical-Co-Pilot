from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class HomeOrganizerResponse(BaseModel):
    summary: str
    checklist: list[str]

def handle_home_organizer_mode(input_text: str) -> HomeOrganizerResponse:
    prompt = f"""
    You are a smart home organization assistant. A user said: "{input_text}"

    Provide a short summary of what they should focus on, and a checklist of tasks to help them organize or clean.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    raw_content = response.choices[0].message.content
    content = raw_content.strip() if raw_content else ""

    if "Checklist:" in content:
        summary, checklist_block = content.split("Checklist:", 1)
        checklist = [line.strip("-• ").strip() for line in checklist_block.strip().splitlines() if line.strip()]
    else:
        summary = content
        checklist = []

    return HomeOrganizerResponse(summary=summary.strip(), checklist=checklist)
