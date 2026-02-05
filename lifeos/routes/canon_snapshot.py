# lifeos/routes/canon_snapshot.py

from lifeos.canon.read_gate import assert_read_allowed
from lifeos.canon.snapshot import build_snapshot
from lifeos.audit.read_audit_hook import audit_read_with_provenance

_POLICY_VERSION = "1.0.0"


def get_snapshot_gpt():
    resource = assert_read_allowed(
        route="/canon/snapshot",
        subject="gpt"
    )
    result = build_snapshot()
    audit_read_with_provenance(
        subject="gpt",
        resource=resource,
        route="/canon/snapshot",
        policy_version=_POLICY_VERSION,
        snapshot_hash=result["integrity"]["snapshot_hash"],
        canon_version=result["integrity"]["canon_version"],
        normalization_version=result["integrity"]["normalization_version"],
    )
    return result
