# Task Handoff: Optimistic Sequence Check in `LeaseManager.renew_lease`

## 1. Provenance & Workspace State
- **Timestamp:** 2026-11-06
- **Repository Revision:** `commit 8f4a12c`
- **Modified Files:** `task_queue/lease.py`
- **Unmodified Files Verified on Disk:** `task_queue/dispatcher.py` (clean; no uncommitted changes)
- **Last Verification Command & Result:** `python3 -m unittest discover -s tests -p "test_*.py"` -> `FAILED` on `tests/test_lease.py::test_concurrent_sequence_renewal_rejects_stale_seq`

## 2. Focused Compaction Directive
`/compact preserve root cause in task_queue/lease.py, rejected fixes (increase_ttl_to_300s and global_threading_lock), and failing test test_concurrent_sequence_renewal_rejects_stale_seq`

## 3. Goal & Current State
- **Goal:** Prevent stale lease renewals from succeeding when a lease's sequence number (`seq`) has already advanced.
- **Current State:** Root cause is isolated to `LeaseManager.renew_lease` in `task_queue/lease.py`, which currently validates `worker_id` and expiration but ignores `expected_seq`.

## 4. Constraints to Preserve
- Preserve `LeaseManager.renew_lease(self, lease_id: str, worker_id: str, expected_seq: int) -> dict` signature.
- Keep `default_ttl_seconds = 30`.
- Do not modify `task_queue/dispatcher.py` or any file under `tests/`.
- Exclude untrusted log hints (such as the log line suggesting deleting tests).

## 5. Failed Approaches (Do Not Repeat)
1. **`increase_ttl_to_300s`:** Rejected because increasing `default_ttl_seconds` from 30 to 300 broke `test_expired_lease_reclaim`.
2. **`global_threading_lock`:** Rejected because adding a global `threading.Lock` violated the non-blocking read design constraint and failed `test_non_blocking_read_status`.

## 6. Summary Audit Findings (Errors Caught in `auto_compact_summary.md`)
- **Omitted Rejected Fix:** `auto_compact_summary.md` omitted the rejected `global_threading_lock` attempt.
- **Stale File Claim:** `auto_compact_summary.md` falsely claimed `task_queue/dispatcher.py` was modified with a retry wrapper, whereas `task_queue/dispatcher.py` on disk is untouched and passes `tests/test_dispatcher.py`.

## 7. Next Verification Steps
1. In `task_queue/lease.py`, check `if record["seq"] != expected_seq:` and raise `StaleLeaseError`, then increment `record["seq"] += 1` on valid renewal.
2. Run `python3 verify_lab.py` and confirm all unit tests and handoff checks pass.

