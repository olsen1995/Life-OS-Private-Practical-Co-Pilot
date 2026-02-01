from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
import logging
import json

from lifeos.routes.canon_router import CanonRouter
from lifeos.gpt.gpt_summarizer import summarize_entity

logger = logging.getLogger("lifeos")

router = APIRouter()
canon_router = CanonRouter()

class CanonQueryRequest(BaseModel):
    type: str

class CanonSearchRequest(BaseModel):
    filters: Optional[Dict[str, str]] = None

class CanonSummarizeRequest(BaseModel):
    type: str
    name: str

@router.post("/canon/query")
async def query_canon(request: CanonQueryRequest):
    entries = canon_router.get_entries_by_type(request.type)
    logger.info(json.dumps({
        "event": "canon_query",
        "type": request.type,
        "results": len(entries)
    }))
    return {"status": "ok", "results": entries}

@router.post("/canon/search")
async def search_canon(request: CanonSearchRequest):
    filters = request.filters or {}
    allowed_keys = {"type", "name", "version"}
    if any(k not in allowed_keys for k in filters):
        raise HTTPException(status_code=400, detail="Invalid filter keys")

    entries = canon_router.get_all_entries()
    results = [entry for entry in entries if all(entry.get(k) == v for k, v in filters.items())]

    logger.info(json.dumps({
        "event": "canon_search",
        "filter_keys": list(filters.keys()),
        "results": len(results)
    }))
    return {"status": "ok", "results": results}

@router.post("/canon/summarize")
async def summarize_canon(request: CanonSummarizeRequest):
    entries = canon_router.get_entries_by_type(request.type)
    entry = next((e for e in entries if e["name"] == request.name), None)
    if not entry:
        raise HTTPException(status_code=404, detail="Entity not found")

    entity = canon_router.get_file_by_path(entry["path"])
    summary = summarize_entity(entity)

    logger.info(json.dumps({
        "event": "canon_summarize",
        "type": request.type,
        "name": request.name
    }))

    return {"status": "ok", "summary": summary}
