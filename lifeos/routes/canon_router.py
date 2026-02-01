from fastapi import APIRouter, HTTPException, Query
import os
import json

CANON_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "canon")
)
MANIFEST_PATH = os.path.join(CANON_ROOT, "Canon_Manifest.json")
TYPES_PATH = os.path.join(CANON_ROOT, "CanonTypes.json")


class CanonRouter:
    """
    Read-only Canon query router.

    Locked constraints:
    - Stateless
    - No runtime imports
    - No validator coupling
    - No Canon mutation
    """

    def __init__(self):
        self.router = APIRouter()

        self.router.add_api_route(
            "/canon/manifest",
            self.get_manifest,
            methods=["GET"],
        )

        self.router.add_api_route(
            "/canon/file",
            self.get_canon_file,
            methods=["GET"],
        )

        self.router.add_api_route(
            "/canon/entries",
            self.get_entries_by_type,
            methods=["GET"],
        )

        self.router.add_api_route(
            "/canon/types",
            self.get_canon_types,
            methods=["GET"],
        )

        self.router.add_api_route(
            "/canon/schema",
            self.get_schema_by_type,
            methods=["GET"],
        )

    def _load_json(self, path: str):
        with open(path, "r") as f:
            return json.load(f)

    def get_manifest(self):
        """
        Return the full Canon_Manifest.json.
        """
        try:
            return self._load_json(MANIFEST_PATH)
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Failed to load Canon manifest.",
            )

    def get_canon_file(self, path: str = Query(..., min_length=1)):
        """
        Return the raw JSON contents of a canon file.

        Constraint:
        - File must be declared in Canon_Manifest.json entries.
        """
        manifest = self.get_manifest()
        valid_paths = {e["path"] for e in manifest.get("entries", [])}

        if path not in valid_paths:
            raise HTTPException(
                status_code=404,
                detail="File not declared in Canon manifest.",
            )

        full_path = os.path.normpath(os.path.join(CANON_ROOT, path))

        if not full_path.startswith(CANON_ROOT):
            raise HTTPException(
                status_code=400,
                detail="Invalid path traversal.",
            )

        if not os.path.isfile(full_path):
            raise HTTPException(
                status_code=404,
                detail="File not found on disk.",
            )

        try:
            return self._load_json(full_path)
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Failed to load canon file.",
            )

    def get_entries_by_type(self, type: str = Query(..., min_length=1)):
        """
        Return manifest entries filtered by CanonType.
        """
        manifest = self.get_manifest()
        return [
            e for e in manifest.get("entries", [])
            if e.get("type") == type
        ]

    def get_canon_types(self):
        """
        Return CanonTypes from CanonTypes.json.

        Constraint:
        - No hardcoded enums.
        """
        try:
            data = self._load_json(TYPES_PATH)
            return data.get("types", [])
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Failed to load CanonTypes.json.",
            )

    def get_schema_by_type(self, type: str = Query(..., min_length=1)):
        """
        Return schema definition for a CanonType.

        Constraint:
        - Only schemas under /lifeos/canon/schemas/
        """
        schema_file = f"{type}.schema.json"
        schema_path = os.path.join(CANON_ROOT, "schemas", schema_file)

        if not os.path.isfile(schema_path):
            raise HTTPException(
                status_code=404,
                detail="Schema not found for CanonType.",
            )

        try:
            return self._load_json(schema_path)
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Failed to load schema file.",
            )
