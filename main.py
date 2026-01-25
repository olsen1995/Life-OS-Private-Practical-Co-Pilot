import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

# Load .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create FastAPI app
app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Optional: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/healthz")
def health_check():
    return {"status": "ok"}

# Root route
@app.get("/")
def root():
    return {"message": "LifeOS CoPilot is running!"}

# Chat endpoint
@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("message", "")

    if not user_message:
        return {"error": "No message provided."}

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are LifeOS, a helpful AI co-pilot."},
                {"role": "user", "content": user_message}
            ]
        )

        # Safely handle possible None
        content = response.choices[0].message.content
        return {"response": content.strip() if content else "[No content returned]"}

    except Exception as e:
        return {"error": str(e)}
