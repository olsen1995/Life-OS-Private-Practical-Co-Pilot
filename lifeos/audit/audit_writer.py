
def write_audit_record(
    *,
    event_type: str,
    subject: str,
    resource: str,
    route: str,
    canon_version: str,
    normalization_version: str,
    policy_version: str,
    snapshot_hash: str | None = None,
    digest_hash: str | None = None,
    provenance: dict | None = None,
) -> None:
    record = {
        "event_type": event_type,
        "subject": subject,
        "resource": resource,
        "route": route,
        "snapshot_hash": snapshot_hash,
        "digest_hash": digest_hash,
        "provenance": provenance,
        "policy_version": policy_version,
        "canon_version": canon_version,
        "normalization_version": normalization_version,
        "timestamp": int(time.time()),
    }

    serialized = _canonical_json(record)
    record["record_hash"] = _hash_record(serialized)

    try:
        _AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with _AUDIT_LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(_canonical_json(record) + "\n")
    except Exception as e:
        print(f"[audit-log-error] {e}", file=sys.stderr)
