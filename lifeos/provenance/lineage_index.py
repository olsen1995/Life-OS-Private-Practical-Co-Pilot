"""
Phase 36 — Lineage Index

Observational only.
Non-authoritative.
Safe to rebuild from audit logs.
"""

import json
import time
from pathlib import Path

_INDEX_PATH = Path("audit_logs/lineage_index.json")


def record_lineage_observation(*, lineage_id: str) -> None:
    try:
        index = {}
        if _INDEX_PATH.exists():
            index = json.loads(_INDEX_PATH.read_text(encoding="utf-8"))

        entry = index.get(lineage_id)
        now = int(time.time())

        if entry is None:
            index[lineage_id] = {
                "first_seen": now,
                "read_count": 1,
            }
        else:
            entry["read_count"] += 1

        _INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        _INDEX_PATH.write_text(
            json.dumps(index, ensure_ascii=False, separators=(",", ":"), sort_keys=True),
            encoding="utf-8",
        )
    except Exception:
        # Silent failure by design
        pass
