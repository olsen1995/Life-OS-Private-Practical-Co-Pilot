from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

# Load environment variables from .env (for local testing)
load_dotenv()

# Read API_KEY from environment
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("API_KEY is not set. Define it in your .env file or hosting environment.")

app = FastAPI()

# ✅ CORS middleware to allow ChatGPT plugin access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve static files including plugin manifest and legal.html
app.mount("/.well-known", StaticFiles(directory="static/well-known"), name="well-known")

# ✅ Core route: /ask
@app.post("/ask")
async def ask(request: Request, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        body = await request.json()
        message = body.get("message", "")
        user_id = body.get("user_id", "default")

        return {
            "user_id": user_id,
            "response": f"You said: '{message}'. I'm here to help with your LifeOS tasks!"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ✅ Health check (optional)
@app.get("/")
def root():
    return {"status": "LifeOS Co-Pilot is running ✅"}
