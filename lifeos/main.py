from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(
    title="LifeOS",
    description="Private Practical Co-Pilot",
    version="0.1.0",
)

# -------------------------------------------------
# Serve OpenAPI schema for GPT Actions
# -------------------------------------------------
app.mount(
    "/.well-known",
    StaticFiles(directory="public/.well-known"),
    name="well-known"
)

# 🌐 Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Runtime state (Canon intentionally disabled)
# -------------------------------------------------

CANON_SYSTEM_IDENTITY = None

FREEZE_FILE = Path("lifeos/FREEZE.json")


@app.get("/")
def root():
    return {
        "status": "ok",
        "canon_identity_loaded": False,
        "canon_identity": None,
    }


@app.get("/meta")
def meta():
    """
    Read-only governance and system status surface.
    """
    return {
        "operational_mode": "Day-2 (Operational)",
        "canon_version": None,
        "canon_digest_loaded": False,
        "freeze_active": FREEZE_FILE.exists(),
    }