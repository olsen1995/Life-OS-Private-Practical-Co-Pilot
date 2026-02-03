from fastapi import APIRouter

healthz_router = APIRouter()

@healthz_router.get("/healthz")
def healthz():
    return {"status": "ok"}
