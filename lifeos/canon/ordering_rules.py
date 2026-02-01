"""
Phase 33 — Declarative Ordering Rules (Executable)

These rules are AUTHORITATIVE.
If CanonRouter output violates assumptions, normalization corrects it.
"""

from typing import Any


def apply_ordering_rules(snapshot: dict) -> dict:
    out = dict(snapshot)

    # Canon root sections — lexicographic
    for key in out:
        if isinstance(out[key], dict):
            out[key] = dict(sorted(out[key].items()))

    # Strategies: preserve declared order (semantic)
    if "strategies" in out and isinstance(out["strategies"], list):
        # preserve source order explicitly
        out["strategies"] = list(out["strategies"])

    # Schemas: lexicographic by id
    if "schemas" in out and isinstance(out["schemas"], list):
        out["schemas"] = sorted(
            out["schemas"],
            key=lambda s: s.get("id", "")
        )

    # Trees: lexicographic by id
    if "trees" in out and isinstance(out["trees"], list):
        out["trees"] = sorted(
            out["trees"],
            key=lambda t: t.get("id", "")
        )

    return out