from fastapi import FastAPI
from mode_router import ModeRouter
from storage.knowledge_loader import KnowledgeLoader
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Initialize ModeRouter
router = ModeRouter()

# Load knowledge
knowledge = KnowledgeLoader().load_all()

class UserInput(BaseModel):
    input: str
    user_id: str = "user_123"  # default

@app.get("/knowledge")
async def list_knowledge():
    return {"loaded_knowledge": list(knowledge.keys())}

@app.post("/route")
async def route_input(data: UserInput):
    mode = router.detect_mode(data.input)
    result = router.handle_mode(mode, data.input, user_id=data.user_id)
    return {"mode": mode, "result": result}
