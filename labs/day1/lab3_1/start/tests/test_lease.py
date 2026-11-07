"""Unit and acceptance tests for task_queue/lease.py."""

import unittest
from task_queue.lease import LeaseManager, StaleLeaseError


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


if __name__ == "__main__":
    unittest.main()

