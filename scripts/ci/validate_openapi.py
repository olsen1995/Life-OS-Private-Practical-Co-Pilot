from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, NoReturn


OPENAPI_FILE = Path("public/.well-known/openapi.json")
EXPECTED_OPENAPI_VERSION = "3.1.0"
EXPECTED_SERVER_SUBSTRING = "https://life-os-private-practical-co-pilot.onrender.com"

REQUIRED: Dict[str, List[str]] = {
    "/ask": ["get", "post"],
    "/memory": ["get", "post", "delete"],
}


def fail(msg: str, code: int = 1) -> NoReturn:
    # NoReturn tells Pylance that execution stops here (so variables are "definitely assigned")
    print(msg)
    raise SystemExit(code)


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        fail(f"❌ ERROR: {path.as_posix()} not found")

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        fail(f"❌ ERROR: invalid JSON in {path.as_posix()} :: {e}")

    if not isinstance(data, dict):
        fail(f"❌ ERROR: root of {path.as_posix()} must be a JSON object")

    return data


def main() -> None:
    data = load_json(OPENAPI_FILE)

    # 1) Basic structure
    if data.get("openapi") != EXPECTED_OPENAPI_VERSION:
        fail(f"❌ ERROR: openapi version must be {EXPECTED_OPENAPI_VERSION}")

    servers = data.get("servers", [])
    if not isinstance(servers, list):
        fail("❌ ERROR: servers must be a list")

    if not any(
        EXPECTED_SERVER_SUBSTRING in (s.get("url", "") if isinstance(s, dict) else "")
        for s in servers
    ):
        fail("❌ ERROR: expected Render server URL not found in servers block")

    paths = data.get("paths", {})
    if not isinstance(paths, dict):
        fail("❌ ERROR: paths must be an object")

    # 2) Check required paths and methods + consequential flag
    missing: List[str] = []

    for path, methods in REQUIRED.items():
        if path not in paths:
            missing.append(f"Missing path: {path}")
            continue

        node = paths[path]
        if not isinstance(node, dict):
            missing.append(f"Path node for {path} must be an object")
            continue

        for method in methods:
            if method not in node:
                missing.append(f"Missing method: {method.upper()} on {path}")
                continue

            op = node[method]
            if not isinstance(op, dict):
                missing.append(f"{method.upper()} on {path} must be an object")
                continue

            if op.get("x-openai-isConsequential") is not False:
                missing.append(
                    f"{method.upper()} on {path} missing x-openai-isConsequential: false"
                )

    if missing:
        for m in missing:
            print("❌", m)
        fail("❌ ERROR: OpenAPI schema failed validation.")

    print("✅ OpenAPI schema is valid.")


if __name__ == "__main__":
    main()
