from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# ✅ Required for GPT Plugin Validation
@app.get("/")
def root():
    return {"status": "OK"}

# ✅ Your main plugin route: /ask
@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    return {"response": f"You asked: {prompt}"}

# ✅ Mount static plugin files (ai-plugin.json, openapi.json, etc.)
app.mount("/.well-known", StaticFiles(directory="static/well-known"), name="well-known")

# 🔐 Optional: check for API key
@app.middleware("http")
async def api_key_auth(request: Request, call_next):
    if request.url.path.startswith("/ask"):
        api_key = request.headers.get("x-api-key")
        expected_key = os.getenv("API_KEY")
        if not api_key or api_key != expected_key:
            return JSONResponse(status_code=401, content={"error": "Unauthorized"})
    return await call_next(request)
