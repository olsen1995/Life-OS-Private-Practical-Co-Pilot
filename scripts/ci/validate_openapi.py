from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, cast


OPENAPI_PATH = Path("public/.well-known/openapi.json")
EXPECTED_SERVER = "https://life-os-private-practical-co-pilot.onrender.com"


def fail(msg: str) -> None:
    print(f"❌ {msg}")
    sys.exit(1)


def load_json(path: Path) -> Dict[str, Any]:
    """
    Load and parse JSON from a file path.
    Pylance-safe: data is always bound; output is guaranteed to be a dict.
    """
    data: Any = {}

    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except FileNotFoundError:
        fail(f"OpenAPI file not found: {path}")
    except json.JSONDecodeError as e:
        fail(f"Invalid JSON in OpenAPI file: {e}")

    if not isinstance(data, dict):
        fail(f"OpenAPI root must be a JSON object: {path}")

    return cast(Dict[str, Any], data)


def main() -> None:
    if not OPENAPI_PATH.exists():
        fail(f"Missing required file: {OPENAPI_PATH}")

    data = load_json(OPENAPI_PATH)

    # Validate OpenAPI version
    if data.get("openapi") != "3.1.0":
        fail("OpenAPI version must be 3.1.0")

    # Validate servers
    servers_any = data.get("servers", [])
    if not isinstance(servers_any, list):
        fail("servers must be a list")

    servers: List[Any] = servers_any

    if not any(
        (s.get("url") == EXPECTED_SERVER) if isinstance(s, dict) else False
        for s in servers
    ):
        fail("Expected Render server URL not found in servers list")

    # Validate required paths/methods
    paths_any = data.get("paths", {})
    if not isinstance(paths_any, dict):
        fail("paths must be an object")

    paths: Dict[str, Any] = paths_any

    required = {
        "/ask": ["get", "post"],
        "/memory": ["get", "post", "delete"],
    }

    for route, methods in required.items():
        if route not in paths:
            fail(f"Missing required path: {route}")

        # Use direct indexing (Pylance-safe after membership check)
        route_obj = paths[route]

        if not isinstance(route_obj, dict):
            fail(f"Path entry must be an object: {route}")

        for method in methods:
            if method not in route_obj:
                fail(f"Missing required method: {method.upper()} {route}")

            # Direct indexing again (guaranteed present)
            op = route_obj[method]

            if not isinstance(op, dict):
                fail(f"Operation must be an object: {method.upper()} {route}")

            if op.get("x-openai-isConsequential") is not False:
                fail(
                    f"Missing or incorrect x-openai-isConsequential flag on {method.upper()} {route}"
                )

    print("✅ OpenAPI schema validation passed.")


if __name__ == "__main__":
    main()
