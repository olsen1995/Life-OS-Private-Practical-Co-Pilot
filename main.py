from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import openai

# Load .env
load_dotenv()

# Get API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY is missing. Please set it in .env or Render.")

# ✅ Create OpenAI client (new v2 syntax)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/ask")
async def ask_question(data: PromptRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": data.prompt}
            ]
        )
        return {"response": response.choices[0].message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/openapi.json")
def get_openapi():
    return FileResponse("openapi.json", media_type="application/json")


@app.get("/")
def root():
    return {
        "message": "✅ Life-OS API is live. Use POST /ask with { 'prompt': 'your question' }."
    }
