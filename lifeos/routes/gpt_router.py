from fastapi import APIRouter, HTTPException, Query
from lifeos.routes.canon_router import CanonRouter

router = APIRouter()
canon_router = CanonRouter()


@router.get("/ask")
def gpt_ready():
    return {
        "status": "ready",
        "model": "LifeOS Co-Pilot",
        "version": "0.1.0",
    }


@router.get("/canon/query")
def gpt_query_canon(
    type: str = Query(..., description="CanonType to query, e.g., LifeOSStrategy"),
):
    try:
        return canon_router.get_entries_by_type(type=type)
    except HTTPException as e:
        raise e
