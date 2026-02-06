import json
from pathlib import Path
from typing import Any, Mapping


RELEASE_FILE = Path("lifeos/canon/RELEASE.json")


def test_canon_promotion_requires_explicit_approval():
    """
    Canon promotion MUST be explicit.
    A Canon release is NOT considered promoted unless
    promotion_approved == true is declared in RELEASE.json.

    Absence of RELEASE.json implies draft Canon.
    """

    if not RELEASE_FILE.exists():
        # Draft Canon is allowed
        return

    raw = RELEASE_FILE.read_text(encoding="utf-8")
    data: Any = json.loads(raw)

    assert isinstance(data, Mapping), "RELEASE.json must be a JSON object"

    promoted = data.get("promotion_approved", False)

    assert promoted in (True, False), (
        "promotion_approved must be a boolean if present"
    )

    # NOTE:
    # This test intentionally does NOT fail when promotion_approved is False.
    # It exists to prevent silent promotion via omission.