"""Unit and acceptance tests for task_queue/lease.py."""

import threading
import unittest
from task_queue.lease import LeaseManager, StaleLeaseError


class _GatedLeases(dict):
    """Lease store that parks the thread named "renewer" on its first lookup.

    This holds a renewal in flight so a test can check whether reads still complete.
    """

    def __init__(self, entered: threading.Event, release: threading.Event) -> None:
        super().__init__()
        self._entered = entered
        self._release = release

    def get(self, key, default=None):
        if threading.current_thread().name == "renewer":
            self._entered.set()
            self._release.wait(timeout=5)
        return super().get(key, default)


class TestLeaseManager(unittest.TestCase):
    def test_acquire_and_expired_lease_reclaim(self) -> None:
        mgr = LeaseManager(default_ttl_seconds=30)
        first = mgr.acquire_lease("job-1", "worker-a", now_ts=100)
        self.assertEqual(first["seq"], 1)
        self.assertEqual(first["expires_at"], 130)

        # Cannot reclaim before t=130
        with self.assertRaises(StaleLeaseError):
            mgr.acquire_lease("job-1", "worker-b", now_ts=120)

        # Reclaiming after 30s expiration succeeds and advances seq to 2
        reclaimed = mgr.acquire_lease("job-1", "worker-b", now_ts=131)
        self.assertEqual(reclaimed["worker_id"], "worker-b")
        self.assertEqual(reclaimed["seq"], 2)

    def test_default_ttl_reclaims_after_30s(self) -> None:
        mgr = LeaseManager()  # the shipped default, not an explicit TTL
        first = mgr.acquire_lease("job-3", "worker-a", now_ts=100)
        self.assertEqual(first["expires_at"], 130)

        # A crashed worker's lease must be reclaimable 31 seconds later
        reclaimed = mgr.acquire_lease("job-3", "worker-b", now_ts=131)
        self.assertEqual(reclaimed["worker_id"], "worker-b")

    def test_concurrent_sequence_renewal_rejects_stale_seq(self) -> None:
        mgr = LeaseManager(default_ttl_seconds=30)
        acquired = mgr.acquire_lease("job-99", "worker-a", now_ts=100)
        self.assertEqual(acquired["seq"], 1)

        # First renewal with expected_seq=1 succeeds and increments seq to 2
        renewed = mgr.renew_lease("job-99", "worker-a", expected_seq=1, now_ts=110)
        self.assertEqual(renewed["seq"], 2)
        self.assertEqual(renewed["expires_at"], 140)

        # Duplicate / delayed renewal request still carrying stale expected_seq=1 must fail
        with self.assertRaises(StaleLeaseError):
            mgr.renew_lease("job-99", "worker-a", expected_seq=1, now_ts=115)

    def test_non_blocking_read_status(self) -> None:
        mgr = LeaseManager(default_ttl_seconds=30)
        mgr.acquire_lease("job-7", "worker-a", now_ts=50)
        status = mgr.get_lease_status("job-7")
        self.assertIsNotNone(status)
        self.assertEqual(status["worker_id"], "worker-a")

        # Hold a renewal in flight, then read from another thread. A lock that
        # serializes every method would make the read wait for the renewal.
        entered, release = threading.Event(), threading.Event()
        gated = _GatedLeases(entered, release)
        gated.update(mgr._leases)
        mgr._leases = gated

        def renew() -> None:
            try:
                mgr.renew_lease("job-7", "worker-a", expected_seq=1, now_ts=60)
            except StaleLeaseError:
                pass

        results: list = []
        renewer = threading.Thread(target=renew, name="renewer")
        reader = threading.Thread(
            target=lambda: results.append(mgr.get_lease_status("job-7")), name="reader"
        )
        renewer.start()
        try:
            self.assertTrue(entered.wait(timeout=2), "renewal never started")
            reader.start()
            reader.join(timeout=1)
            blocked = reader.is_alive()
        finally:
            release.set()
            renewer.join(timeout=5)
            if reader.ident is not None:
                reader.join(timeout=5)
        self.assertFalse(blocked, "read blocked while a renewal was in flight")


if __name__ == "__main__":
    unittest.main()
