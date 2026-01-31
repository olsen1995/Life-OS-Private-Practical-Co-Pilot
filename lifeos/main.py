from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lifeos.routes.mode_router import ModeRouter

app = FastAPI()

# 🌐 Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount ModeRouter via composition
router = ModeRouter()
app.include_router(router.router, prefix="")

# 🩺 Health check route
@app.get("/health")
def health_check():
    return {"status": "ok"}
