from typing import Mapping, Any

from lifeos.canon.snapshot import get_snapshot
from lifeos.canon.digest import compute_canon_digest


def test_snapshot_declares_version():
    """
    Canon snapshots must explicitly declare a version.
    Consumers may not rely on implicit or inferred versions.
    """
    snapshot = get_snapshot()

    assert isinstance(snapshot, Mapping), "Snapshot must be a mapping"
    assert "version" in snapshot, "Snapshot missing required 'version' field"
    assert snapshot["version"], "Snapshot 'version' must be non-empty"


def test_snapshot_digest_includes_version_identity():
    """
    Canon digest must be version-aware so snapshot compatibility
    cannot drift silently across releases.
    """
    snapshot = get_snapshot()
    digest = compute_canon_digest(snapshot)

    assert isinstance(digest, Mapping), "Digest must be a mapping"
    assert "version" in digest, "Digest missing required 'version' identity"
    assert (
        digest["version"] == snapshot["version"]
    ), "Digest version must match snapshot version"