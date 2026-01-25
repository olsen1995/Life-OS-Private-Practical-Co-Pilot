# main.py

import sys
from pathlib import Path

# Ensure the repo root is in sys.path so imports work correctly
sys.path.append(str(Path(__file__).parent.resolve()))

from fastapi import FastAPI
from pydantic import BaseModel

# Import ModeRouter after fixing sys.path
from mode_router import ModeRouter
from storage.knowledge_loader import KnowledgeLoader

import openai
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI()

# Load knowledge once for all modes
knowledge = KnowledgeLoader().load_all()

# Initialize ModeRouter
router = ModeRouter()

# Pydantic model for user input
class UserInput(BaseModel):
    input: str
    user_id: str = "user_123"  # default

# Endpoint to list all loaded knowledge
@app.get("/knowledge")
async def list_knowledge():
    return {"loaded_knowledge": list(knowledge.keys())}

# Endpoint to route input to the correct mode
@app.post("/route")
async def route_input(data: UserInput):
    mode = router.detect_mode(data.input)
    result = router.handle_mode(mode, data.input, user_id=data.user_id)
    return {"mode": mode, "result": result}

@app.post("/chat")
async def chat_endpoint(data: UserInput):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant named LifeOS."},
                {"role": "user", "content": data.input}
            ]
        )
        return {"response": response.choices[0].message["content"]}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
