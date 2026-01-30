import os
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client (SDK v1+)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def generate_weekly_schedule(tasks: List[str]) -> Dict[str, List[str]]:
    """
    Distribute tasks across the week, one per day starting from Monday.
    Always returns Dict[str, List[str]].
    """
    if not tasks:
        return {"Error": ["No tasks provided."]}

    schedule: Dict[str, List[str]] = {day: [] for day in DAYS}

    for i, task in enumerate(tasks):
        day = DAYS[i % len(DAYS)]
        hour = 9 + (i % 8)  # 9am–4pm
        schedule[day].append(f"{hour}:00 - {task}")

    return schedule


def extract_tasks_with_gpt(user_input: str) -> List[str]:
    """
    Uses GPT to extract a clean list of tasks from natural language input.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract 5–10 short, actionable personal tasks from the user's input. "
                        "Return ONLY a plain list of tasks, one per line. No explanations."
                    ),
                },
                {"role": "user", "content": user_input},
            ],
            max_tokens=200,
            temperature=0.4,
        )

        content = response.choices[0].message.content or ""
        tasks = [
            line.strip("-• ").strip()
            for line in content.splitlines()
            if line.strip()
        ]

        return tasks

    except Exception as e:
        return [f"Failed to extract tasks: {str(e)}"]


def handle_dayplanner_mode(user_input: str) -> Dict[str, List[str]]:
    """
    GPT-powered DayPlanner:
    1. Extract tasks with GPT
    2. Generate a weekly schedule
    """
    tasks = extract_tasks_with_gpt(user_input)
    return generate_weekly_schedule(tasks)
