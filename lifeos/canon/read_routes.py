# lifeos/canon/read_routes.py
"""
Phase 34 — Canon Read Route Registry

Every Canon read route MUST be declared here.
CI enforces exhaustiveness.
"""

READ_ROUTES = {
    "/canon/snapshot": "snapshot",
    "/canon/snapshot/digest": "digest",
    "/canon/schemas": "schemas",
    "/canon/trees": "trees",
}
