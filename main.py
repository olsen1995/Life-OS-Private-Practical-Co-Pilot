
import os
from typing import Optional, Any

from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from openai import OpenAI

from auth_manager import verify_api_key, get_api_key_info
from mode_router import ModeRouter
from response_formatter import format_response, format_error, chunk_for_adhd
from storage.memory_manager import MemoryManager

# Load environment variables
load_dotenv()

api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("❌ OPENAI_API_KEY is missing. Set it in .env or Render environment.")

client = OpenAI(api_key=api_key)

# FastAPI app
app = FastAPI()
router = ModeRouter(openai_client=client)
templates = Jinja2Templates(directory="templates")

@app.post("/ask")
async def ask(request: Request, x_api_key: str = Depends(verify_api_key)):
    try:
        data = await request.json()
        user_message = data.get("message", "")
        user_id = data.get("user_id", "user_123")
        adhd_mode = data.get("adhd_mode", False)

        mode = router.route_request(user_message)
        raw_result = router.handle_mode(mode, user_message, user_id=user_id)

        response_data = raw_result.dict() if hasattr(raw_result, "dict") else dict(raw_result)
        summary = response_data.get("summary", "Here's the result.")
        steps = response_data.get("steps", [])
        actions = response_data.get("actions", [])
        priority = response_data.get("priority", "normal")

        return (
            chunk_for_adhd(summary, steps, actions)
            if adhd_mode else
            format_response(summary, steps, priority, actions)
        )

    except Exception as e:
        return format_error(str(e))


@app.get("/memory", response_class=HTMLResponse)
async def memory_dashboard(request: Request, user_id: str = "user_123"):
    mm = MemoryManager(user_id)
    return templates.TemplateResponse("memory.html", {
        "request": request,
        "user_id": user_id,
        "memories": mm.get_all()
    })

@app.post("/memory", response_class=RedirectResponse)
async def clear_memory(request: Request, user_id: str = "user_123", confirm: str = Form("no")):
    mm = MemoryManager(user_id)
    if confirm == "yes":
        mm.delete_all()
    return RedirectResponse(f"/memory?user_id={user_id}", status_code=303)

@app.get("/api-keys", response_class=HTMLResponse)
async def show_api_keys(request: Request):
    api_keys = get_api_key_info()
    return templates.TemplateResponse("api_keys.html", {
        "request": request,
        "api_keys": api_keys
    })
