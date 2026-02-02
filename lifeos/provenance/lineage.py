"""
Phase 36 — Lineage Derivation

Pure, deterministic, non-authoritative.
NEVER used for gating or decisions.
"""

import hashlib


def derive_lineage_id(
    *,
    canon_version: str,
    snapshot_hash: str,
    normalization_version: str,
) -> str:
    payload = f"{canon_version}|{snapshot_hash}|{normalization_version}"
    h = hashlib.sha256()
    h.update(payload.encode("utf-8"))
    return f"sha256:{h.hexdigest()}"
