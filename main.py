import os
from typing import Optional, Any

from fastapi import FastAPI, Request
from dotenv import load_dotenv
from openai import OpenAI

from mode_router import ModeRouter
from response_formatter import (
    format_response,
    format_error,
    chunk_for_adhd,
)

# ------------------------------------------------------------
# Load environment variables
# ------------------------------------------------------------
load_dotenv()

api_key: Optional[str] = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "❌ OPENAI_API_KEY is missing.\n"
        "➡️ Set it in Render Environment or your local .env file."
    )

# ------------------------------------------------------------
# Initialize OpenAI SDK Client
# ------------------------------------------------------------
client = OpenAI(api_key=api_key)

# ------------------------------------------------------------
# FastAPI App Setup
# ------------------------------------------------------------
app = FastAPI()

# ------------------------------------------------------------
# Mode Router Instance
# ------------------------------------------------------------
router = ModeRouter()

# ------------------------------------------------------------
# Main /ask endpoint
# ------------------------------------------------------------
@app.post("/ask")
async def ask(request: Request):
    try:
        data = await request.json()
        user_message: str = data.get("message", "")
        user_id: str = data.get("user_id", "user_123")
        adhd_mode: bool = data.get("adhd_mode", False)

        mode = router.route_request(user_message)

        # Get the response and normalize to dict
        raw_result: Any = router.handle_mode(mode, user_message, user_id=user_id)
        if hasattr(raw_result, "dict"):
            response_data = raw_result.dict()
        else:
            response_data = dict(raw_result) if isinstance(raw_result, dict) else {}

        summary = response_data.get("summary", "Here's the result.")
        steps = response_data.get("steps", [])
        actions = response_data.get("actions", [])
        priority = response_data.get("priority", "normal")

        if adhd_mode:
            return chunk_for_adhd(summary=summary, steps=steps, actions=actions)
        else:
            return format_response(summary=summary, steps=steps, priority=priority, actions=actions)

    except Exception as e:
        return format_error(str(e))


# ------------------------------------------------------------
# Start the scheduler
# ------------------------------------------------------------
from scheduler import start_scheduler
start_scheduler()
