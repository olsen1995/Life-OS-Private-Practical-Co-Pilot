
import os
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

from mode_router import ModeRouter
from response_formatter import format_response, format_error, chunk_for_adhd

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

# Optional CORS setup (uncomment if needed)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

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
        user_message = data.get("message", "")
        user_id = data.get("user_id", "user_123")
        adhd_mode = data.get("adhd_mode", False)

        mode = router.route_request(user_message)
        response_data = router.handle_mode(mode, user_message, user_id=user_id)

        if adhd_mode:
            return chunk_for_adhd(
                summary=response_data.get("summary", "Here's the info."),
                steps=response_data.get("steps", []),
                actions=response_data.get("actions", [])
            )
        else:
            return format_response(
                summary=response_data.get("summary", "Here's the result."),
                steps=response_data.get("steps", []),
                priority=response_data.get("priority", "normal"),
                actions=response_data.get("actions", [])
            )

    except Exception as e:
        return format_error(str(e))
