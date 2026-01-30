from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("API_KEY is not set. Define it in your .env file or hosting environment.")

app = FastAPI()

# Allow CORS for plugin calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ You can restrict this to your plugin domain if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask_handler(request: Request, x_api_key: str = Header(None)):
    # 🔐 Validate API Key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        data = await request.json()
        message = data.get("message", "")
        user_id = data.get("user_id", "unknown")

        # 🔁 Simulate response (replace this logic with your actual task/memory engine)
        return {
            "user_id": user_id,
            "response": f"Hi! You said: '{message}' — I'm ready to help you with LifeOS tasks."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
