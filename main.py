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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
