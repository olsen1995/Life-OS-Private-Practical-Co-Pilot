from fastapi import APIRouter

from lifeos.canon.digest import get_digest
from lifeos.canon.schemas import get_schemas
from lifeos.canon.snapshot import get_snapshot
from lifeos.canon.trees import get_trees


class CanonRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/canon")

        self.router.add_api_route(
            "/snapshot",
            get_snapshot,
            methods=["GET"],
            tags=["canon"],
        )
        self.router.add_api_route(
            "/digest",
            get_digest,
            methods=["GET"],
            tags=["canon"],
        )
        self.router.add_api_route(
            "/schemas",
            get_schemas,
            methods=["GET"],
            tags=["canon"],
        )
        self.router.add_api_route(
            "/trees",
            get_trees,
            methods=["GET"],
            tags=["canon"],
        )
