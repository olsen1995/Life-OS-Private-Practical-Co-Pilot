import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Load environment variables from .env (for local dev)
load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("API_KEY is not set. Define it in your .env or Render environment.")

app = FastAPI()

# ✅ Required CORS headers for ChatGPT plugin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, lock this down to https://chat.openai.com
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount static folder for .well-known files
app.mount("/.well-known", StaticFiles(directory="static/well-known"), name="well-known")

# ✅ /ask endpoint used in plugin
@app.post("/ask")
async def ask(request: Request):
    # Auth
    x_api_key = request.headers.get("x-api-key")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    # Request body
    body = await request.json()
    prompt = body.get("prompt")

    if not prompt:
        raise HTTPException(status_code=400, detail="Missing 'prompt' in request")

    # Simulated response
    return JSONResponse(content={
        "response": f"✅ LifeOS heard you say: '{prompt}'. This is your assistant's reply!"
    })

# ✅ Optional healthcheck
@app.get("/")
def root():
    return {"status": "LifeOS Co-Pilot is running"}
