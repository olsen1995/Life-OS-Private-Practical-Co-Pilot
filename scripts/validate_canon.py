"""
Canon Validator — CI Only

Scope:
- CI path alignment only
- No Canon mutation
- No runtime behavior changes
"""

from pathlib import Path


def validate_canon_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    canon_root = repo_root / "lifeos" / "canon"

    if not canon_root.exists():
        raise FileNotFoundError(f"Canon directory not found: {canon_root}")

    manifests = list(canon_root.glob("Canon_Manifest_*.json"))

    if len(manifests) == 0:
        raise FileNotFoundError(
            f"No Canon_Manifest_*.json found in {canon_root}"
        )

    if len(manifests) > 1:
        raise RuntimeError(
            f"Multiple Canon manifests found (expected exactly one): {manifests}"
        )

    # Exactly one manifest — success
    manifest_path = manifests[0]
    print(f"Canon manifest resolved: {manifest_path}")


if __name__ == "__main__":
    validate_canon_manifest()
    print("Canon manifest validation passed.")
