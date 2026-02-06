import json
import subprocess
from pathlib import Path
from typing import Any, Mapping


FREEZE_FILE = Path("lifeos/FREEZE.json")
CANON_PATH = Path("lifeos/canon")

REQUIRED_OVERRIDE_FIELDS = {
    "override",
    "override_by",
    "override_reason",
    "override_timestamp",
}


def _git_diff_exists(path: Path) -> bool:
    """
    Returns True if git reports changes under the given path.
    """
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "--", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    return bool(result.stdout.strip())


def _has_valid_override(data: Mapping[str, Any]) -> bool:
    """
    Validate that an emergency override is explicit, complete, and auditable.
    """
    if data.get("override") is not True:
        return False

    missing = REQUIRED_OVERRIDE_FIELDS - set(data.keys())
    if missing:
        raise AssertionError(
            "Freeze override is incomplete. Missing fields:\n"
            + "\n".join(sorted(missing))
        )

    for field in REQUIRED_OVERRIDE_FIELDS:
        assert data[field], f"Override field '{field}' must be non-empty"

    return True


def test_canon_is_immutable_when_frozen_with_audited_override():
    """
    Canon must not change when a freeze is active unless
    an explicit, fully-audited override is declared.
    """

    if not FREEZE_FILE.exists():
        # No freeze declared — Canon changes allowed
        return

    data: Any = json.loads(FREEZE_FILE.read_text(encoding="utf-8"))
    assert isinstance(data, Mapping), "FREEZE.json must be a JSON object"

    scope = data.get("scope")

    if scope not in {"canon", "global"}:
        # Freeze does not apply to Canon
        return

    if _has_valid_override(data):
        # Explicit, audited override allows Canon changes
        return

    assert not _git_diff_exists(CANON_PATH), (
        "Canon is frozen and no valid emergency override is present. "
        "Either remove the freeze or declare a full audited override."
    )