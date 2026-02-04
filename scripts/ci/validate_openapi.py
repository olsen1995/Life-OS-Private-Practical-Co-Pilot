import json
import sys
from pathlib import Path
from typing import Any


FILE = Path("public/.well-known/openapi.json")
EXPECTED_SERVER = "https://life-os-private-practical-co-pilot.onrender.com"

REQUIRED = {
    "/ask": ["get", "post"],
    "/memory": ["get", "post", "delete"],
}


def fail(msg: str) -> None:
    print(f"❌ {msg}")
    sys.exit(1)


def main() -> None:
    if not FILE.exists():
        fail(f"{FILE} not found")

    data: dict[str, Any] = {}

    try:
        data = json.loads(FILE.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"Failed to parse JSON: {e}")

    if data.get("openapi") != "3.1.0":
        fail("openapi version must be 3.1.0")

    servers = data.get("servers", [])
    if not any(EXPECTED_SERVER in (s.get("url", "") or "") for s in servers):
        fail("expected Render server URL not found in servers block")

    paths = data.get("paths") or {}
    missing: list[str] = []

    for path, methods in REQUIRED.items():
        if path not in paths:
            missing.append(f"Missing path: {path}")
            continue

        for method in methods:
            if method not in paths[path]:
                missing.append(f"Missing method: {method.upper()} on {path}")
                continue

            op = paths[path][method]
            if op.get("x-openai-isConsequential") is not False:
                missing.append(
                    f"{method.upper()} on {path} missing x-openai-isConsequential: false"
                )

    if missing:
        print("❌ OpenAPI schema failed validation:")
        for m in missing:
            print("❌", m)
        sys.exit(1)

    print("✅ OpenAPI schema is valid.")


if __name__ == "__main__":
    main()
