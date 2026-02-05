import json
import re
from pathlib import Path


CANON_PATHS = [
    Path("lifeos/canon/trees"),
    Path("lifeos/canon/strategies"),
    Path("lifeos/canon/schemas"),
]

REQUIRED_KEYS = ["id", "title", "version"]

ID_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def test_all_json_files_have_ordered_keys_and_required_fields():
    for base_path in CANON_PATHS:
        for path in base_path.rglob("*.json"):
            raw = path.read_text(encoding="utf-8")
            data = json.loads(raw)

            # Key order check
            keys = list(data.keys())
            if keys != sorted(keys):
                raise AssertionError(f"Unordered keys in {path}")

            # Required field check
            for key in REQUIRED_KEYS:
                if key not in data:
                    raise AssertionError(f"Missing required key '{key}' in {path}")

            # ID format check
            _id = data["id"]
            if not isinstance(_id, str) or not ID_PATTERN.match(_id):
                raise AssertionError(f"Invalid ID format in {path}: {_id}")
