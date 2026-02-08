"""
Canon JSON Loader Utility

Purpose:
- Provide a single, explicit utility for loading Canon JSON files
- Read-only
- No access control
- No policy enforcement
- No runtime assumptions

This module introduces capability ONLY.
It is not wired into runtime, governance, or CI.
"""

import json
from pathlib import Path


class CanonLoadError(Exception):
    """Raised when a Canon file cannot be loaded or parsed."""
    pass


def load_canon_json(relative_path: str) -> dict:
    """
    Load a Canon JSON file by relative path.

    Args:
        relative_path: Path relative to lifeos/canon/

    Returns:
        Parsed JSON as dict

    Raises:
        CanonLoadError: if file is missing, unreadable, or invalid JSON
    """
    canon_root = Path("lifeos/canon")
    target = canon_root / relative_path

    if not target.exists():
        raise CanonLoadError(f"Canon file not found: {target}")

    try:
        return json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CanonLoadError(
            f"Invalid JSON in Canon file: {target}"
        ) from exc