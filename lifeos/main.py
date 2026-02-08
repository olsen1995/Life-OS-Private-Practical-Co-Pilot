from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

# 🧠 Canon read-gate (existing utility)
from lifeos.canon.read_gate import read_canon_file

app = FastAPI(
    title="LifeOS",
    description="Private Practical Co-Pilot",
    version="0.1.0",
)

# 🌐 Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------
# 🔬 RUNTIME CANON READ PILOT (M17.2)
# -------------------------------------------------------------------

CANON_SYSTEM_IDENTITY = None

try:
    CANON_SYSTEM_IDENTITY = read_canon_file(
        "metadata/system_identity.json"
    )
except Exception:
    CANON_SYSTEM_IDENTITY = None


# -------------------------------------------------------------------
# 🔎 GOVERNANCE STATUS VISIBILITY (M18.1)
#
# Read-only surface.
# No enforcement.
# No coupling.
# Optional data only.
# -------------------------------------------------------------------

FREEZE_FILE = Path("lifeos/FREEZE.json")

CANON_DIGEST = None
try:
    CANON_DIGEST = read_canon_file("snapshot_digest.json")
except Exception:
    CANON_DIGEST = None


@app.get("/")
def root():
    return {
        "status": "ok",
        "canon_identity_loaded": CANON_SYSTEM_IDENTITY is not None,
        "canon_identity": CANON_SYSTEM_IDENTITY,
    }


@app.get("/meta")
def meta():
    """
    Read-only governance and system status surface.
    """
    return {
        "operational_mode": "Day-2 (Operational)",
        "canon_version": (
            CANON_SYSTEM_IDENTITY.get("version")
            if isinstance(CANON_SYSTEM_IDENTITY, dict)
            else None
        ),
        "canon_digest_loaded": CANON_DIGEST is not None,
        "freeze_active": FREEZE_FILE.exists(),
    }