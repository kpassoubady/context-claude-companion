"""Optimistic sequence-number lease manager for task_queue."""


class StaleLeaseError(RuntimeError):
    """Raised when a worker attempts to renew a lease with a stale sequence number or expired state."""


class LeaseManager:
    """Manage worker leases using optimistic sequence numbers (`seq`)."""

    def __init__(self, default_ttl_seconds: int = 30) -> None:
        self.default_ttl_seconds = default_ttl_seconds
        self._leases: dict[str, dict[str, int | str]] = {}

    def acquire_lease(self, lease_id: str, worker_id: str, now_ts: int) -> dict[str, int | str]:
        """Acquire a new lease or reclaim an expired lease, incrementing `seq`."""
        existing = self._leases.get(lease_id)
        if existing is not None and int(existing["expires_at"]) > now_ts:
            raise StaleLeaseError(f"Lease {lease_id} is currently active until {existing['expires_at']}")
        next_seq = 1 if existing is None else int(existing["seq"]) + 1
        record: dict[str, int | str] = {
            "lease_id": lease_id,
            "worker_id": worker_id,
            "seq": next_seq,
            "expires_at": now_ts + self.default_ttl_seconds,
        }
        self._leases[lease_id] = record
        return dict(record)

    def renew_lease(self, lease_id: str, worker_id: str, expected_seq: int, now_ts: int = 100) -> dict[str, int | str]:
        """Renew an active lease only if `worker_id` and `expected_seq` match current state."""
        record = self._leases.get(lease_id)
        if record is None:
            raise StaleLeaseError(f"Unknown lease: {lease_id}")
        if int(record["expires_at"]) <= now_ts:
            raise StaleLeaseError(f"Lease {lease_id} already expired at {record['expires_at']}")
        if record["worker_id"] != worker_id:
            raise StaleLeaseError(f"Lease {lease_id} is owned by {record['worker_id']}, not {worker_id}")
        if int(record["seq"]) != expected_seq:
            raise StaleLeaseError(
                f"Stale sequence {expected_seq} for lease {lease_id}; current seq is {record['seq']}"
            )

        record["seq"] = int(record["seq"]) + 1
        record["expires_at"] = now_ts + self.default_ttl_seconds
        return dict(record)

    def get_lease_status(self, lease_id: str) -> dict[str, int | str] | None:
        """Non-blocking read of current lease metadata."""
        record = self._leases.get(lease_id)
        return dict(record) if record is not None else None

