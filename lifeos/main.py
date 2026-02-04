from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# ─────────────────────────────────────────────────────────────
# FastAPI App
# ─────────────────────────────────────────────────────────────

app = FastAPI(
    title="LifeOS Co-Pilot API",
    version="2.0.1",
    servers=[
        {
            "url": "https://life-os-private-practical-co-pilot.onrender.com"
        }
    ]
)


@app.get("/.well-known/openapi.json", include_in_schema=False)
def openapi_static():
    root = Path(__file__).resolve().parents[1]
    f = root / "public" / ".well-known" / "openapi.json"
    return FileResponse(str(f), media_type="application/json")


# ─────────────────────────────────────────────────────────────
# Middleware
# ─────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────────────────────
# Routers (absolute package imports for local uvicorn)
# ─────────────────────────────────────────────────────────────

from lifeos.routes.mode_router import ModeRouter
from lifeos.routes.memory_read_router import router as memory_read_router
from lifeos.routes.healthz import healthz_router

router = ModeRouter()

app.include_router(router.router)
app.include_router(memory_read_router)
app.include_router(healthz_router)
