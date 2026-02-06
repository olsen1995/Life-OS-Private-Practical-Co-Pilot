import json
from pathlib import Path
from typing import Mapping, Any


RELEASE_FILE = Path("lifeos/canon/RELEASE.json")

REQUIRED_FIELDS = {
    "release_id",
    "canon_version",
    "snapshot_version",
    "snapshot_digest",
    "released_at",
}


def test_canon_release_model_is_explicit_and_valid():
    """
    Canon releases must be explicitly declared.
    If a RELEASE.json exists, it must be complete and well-formed.
    Absence of RELEASE.json indicates a working (unreleased) Canon tree.
    """

    if not RELEASE_FILE.exists():
        # Working tree is allowed — no release declared yet
        return

    raw = RELEASE_FILE.read_text(encoding="utf-8")
    data: Any = json.loads(raw)

    assert isinstance(data, Mapping), "RELEASE.json must be a JSON object"

    missing = REQUIRED_FIELDS - set(data.keys())
    assert not missing, (
        "Canon release metadata is incomplete. Missing fields:\n"
        + "\n".join(sorted(missing))
    )

    for field in REQUIRED_FIELDS:
        assert data[field], f"Release field '{field}' must be non-empty"