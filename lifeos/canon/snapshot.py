from lifeos.canon.router import CanonRouter
from lifeos.canon.normalization import (
    normalize,
    normalize_to_bytes,
    NORMALIZATION_VERSION,
)
from lifeos.canon.hash_utils import sha256_bytes


def build_snapshot():
    raw = CanonRouter.get_snapshot()
    normalized = normalize(raw)
    snapshot_hash = sha256_bytes(normalize_to_bytes(raw))

    return {
        "data": normalized,
        "integrity": {
            "snapshot_hash": snapshot_hash,
            "canon_version": CanonRouter.canon_version(),
            "normalization_version": NORMALIZATION_VERSION,
        },
    }


def build_digest():
    raw = CanonRouter.get_digest()
    normalized = normalize(raw)
    digest_hash = sha256_bytes(normalize_to_bytes(raw))

    return {
        "data": normalized,
        "integrity": {
            "digest_hash": digest_hash,
            "canon_version": CanonRouter.canon_version(),
            "normalization_version": NORMALIZATION_VERSION,
        },
    }