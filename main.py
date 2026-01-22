from fastapi import FastAPI
from pydantic import BaseModel
from mode_router import ModeRouter

app = FastAPI()
router = ModeRouter()

class UserInput(BaseModel):
    input: str

@app.post("/route")
async def route_input(data: UserInput):
    mode = router.detect_mode(data.input)
    return {"mode": mode}
