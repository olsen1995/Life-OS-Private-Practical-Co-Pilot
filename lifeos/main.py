from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lifeos.routes.canon_router import CanonRouter

app = FastAPI()

# 🌐 Temporary CORS config for Render compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict CORS in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# 📦 Mount Canon read-only router under /canon
canon_router = CanonRouter()
app.include_router(canon_router.router, prefix="/canon")

# 🟢 Startup log
print("✅ LifeOS Co-Pilot API booted successfully")
