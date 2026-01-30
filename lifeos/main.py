from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os

# ✅ Import routers (after moving routes/ into lifeos/)
from lifeos.routes.healthz import router as healthz_router

app = FastAPI()

@app.get("/")
def root():
    return {"status": "running"}

# 🔐 API Key middleware for protected endpoints like /ask
@app.middleware("http")
async def check_api_key(request: Request, call_next):
    if request.url.path == "/ask":
        api_key = request.headers.get("x-api-key")
        expected_key = os.getenv("API_KEY")
        if api_key != expected_key:
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    return await call_next(request)

# ✅ Example protected route
@app.post("/ask")
async def ask(message: dict):
    return {"response": f"You asked: {message['message']}"}

# ✅ Serve static files (unchanged)
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="well-known")

# ✅ Include routers
app.include_router(healthz_router)
