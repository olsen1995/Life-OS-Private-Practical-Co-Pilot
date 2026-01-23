from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from mode_router import ModeRouter, run_mode_logic

# Initialize FastAPI app
app = FastAPI()

# Serve .well-known for plugin manifest
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")

# Initialize the ModeRouter
router = ModeRouter()

# Input model
class UserInput(BaseModel):
    input: str

# Endpoint for routing user input to a mode
@app.post("/route")
async def route_input(data: UserInput):
    mode = router.detect_mode(data.input)
    result = run_mode_logic(mode, data.input)
    return {
        "mode": mode,
        "result": result
    }

# Inject OpenAPI "servers" field so GPT plugin accepts the schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="LifeOS Co-Pilot",
        version="1.0.0",
        description="Routes your input to real-life task modes.",
        routes=app.routes,
    )
    openapi_schema["servers"] = [
        {"url": "https://zeke-unattaining-wendy.ngrok-free.dev"}  # Replace this URL when deployed
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
