from lifeos.canon.read_gate import assert_read_allowed
from lifeos.canon.snapshot import build_snapshot


def get_snapshot_internal():
    assert_read_allowed(
        route="/canon/snapshot",
        subject="internal"
    )
    return build_snapshot()


def get_snapshot_gpt():
    assert_read_allowed(
        route="/canon/snapshot",
        subject="gpt"
    )
    return build_snapshot()


def get_snapshot_external():
    assert_read_allowed(
        route="/canon/snapshot",
        subject="external"
    )
    return build_snapshot()
