# lifeos/routes/canon_digest.py

from lifeos.canon.read_gate import assert_read_allowed
from lifeos.canon.snapshot import build_digest
from lifeos.audit.read_audit_hook import audit_read_with_provenance

_POLICY_VERSION = "1.0.0"


def get_digest_internal():
    resource = assert_read_allowed(
        route="/canon/snapshot/digest",
        subject="internal"
    )
    result = build_digest()
    audit_read_with_provenance(
        subject="internal",
        resource=resource,
        route="/canon/snapshot/digest",
        policy_version=_POLICY_VERSION,
        digest_hash=result["integrity"]["digest_hash"],
        canon_version=result["integrity"]["canon_version"],
        normalization_version=result["integrity"]["normalization_version"],
    )
    return result
