from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from mode_router import ModeRouter

# Initialize FastAPI app
app = FastAPI()

# Mount static directory for GPT plugin manifest
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")

# Initialize the router
router = ModeRouter()

# Define input model
class UserInput(BaseModel):
    input: str

# Define /route endpoint
@app.post("/route")
async def route_input(data: UserInput):
    mode = router.detect_mode(data.input)
    return {"mode": mode}
