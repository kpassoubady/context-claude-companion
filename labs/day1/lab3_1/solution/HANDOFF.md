# Task Handoff: Optimistic Sequence Check in `LeaseManager.renew_lease`

## 1. Provenance & Workspace State
- **Timestamp:** 2026-11-06
- **Repository Revision:** `e2dca69` (baseline commit from `./setup_repo.sh`; the hash is that of this solution tree)
- **Modified Files:** `task_queue/lease.py` (`git status --short` lists `M task_queue/lease.py`)
- **Unmodified Files Verified on Disk:** `task_queue/dispatcher.py` (not listed by `git status`, so clean) and everything under `tests/`
- **Last Verification Command & Result:** `python3 -m unittest discover -s tests -p "test_*.py"` -> `FAILED` on `tests/test_lease.py::test_concurrent_sequence_renewal_rejects_stale_seq`

## 2. Focused Compaction Directive
`/compact preserve the root cause in task_queue/lease.py (renew_lease ignores expected_seq), both rejected fixes (increase_ttl_to_300s, global_threading_lock) with the test each broke, and the failing test test_concurrent_sequence_renewal_rejects_stale_seq`
- **Result of running it:** the live summary kept the root cause and both rejected fixes with their test names, and dropped the Turn 31 log line entirely. The supplied auto summary kept only the TTL attempt and invented a retry patch.

## 3. Goal & Current State
- **Goal:** Prevent stale lease renewals from succeeding when a lease's sequence number (`seq`) has already advanced.
- **Current State:** Root cause is isolated to `LeaseManager.renew_lease` in `task_queue/lease.py`, which validates `worker_id` and expiration but never compares `expected_seq` and never increments `seq`.

## 4. Constraints to Preserve
- Preserve `LeaseManager.renew_lease(self, lease_id: str, worker_id: str, expected_seq: int) -> dict` signature.
- Keep `default_ttl_seconds = 30`.
- Do not modify `task_queue/dispatcher.py` or any file under `tests/`.
- Exclude untrusted log hints from the transcript (Turn 31 asked to remove a test; it was not acted on).

## 5. Failed Approaches (Do Not Repeat)
1. **`increase_ttl_to_300s`:** raising `default_ttl_seconds` from 30 to 300 broke `test_default_ttl_reclaims_after_30s`, because a crashed worker's lease stayed held for five minutes.
2. **`global_threading_lock`:** one `threading.Lock` around every method broke `test_non_blocking_read_status`, because a status read waited for a renewal in flight.

## 6. Summary Audit Findings (Errors Caught in `auto_compact_summary.md`)
- **Finding 1 (wrong value):** the summary says `default_ttl_seconds = 60` was settled on; `task_queue/lease.py` still has 30 and the transcript says the TTL was reverted to 30, so the 60 never existed.
- **Finding 2 (false file claim):** the summary says `task_queue/dispatcher.py` got a retry wrapper; `git status` does not list it and the transcript's Turn 34 status calls it clean.
- **Finding 3 (omission):** the summary leaves out the `global_threading_lock` rejection and the test it broke, so a fresh session could propose the lock again.

## 7. Next Verification Steps
1. In `task_queue/lease.py`, raise `StaleLeaseError` when `record["seq"] != expected_seq`, then increment `record["seq"]` on valid renewal.
2. Run `python3 verify_lab.py` and confirm all unit tests and handoff checks pass.

## 8. Fresh-Session Verification
- **Read at session start:** `CLAUDE.md`, `HANDOFF.md`, `task_queue/lease.py`, `tests/test_lease.py`.
- **Disk checks run:** `git status --short` listed only `M task_queue/lease.py` and `?? HANDOFF.md`; `python3 -m unittest discover -s tests -p "test_*.py"` ran 5 tests with 1 failure, `test_concurrent_sequence_renewal_rejects_stale_seq`.
- **One fact found wrong or stale:** the auto summary's claim that `dispatcher.py` was modified; `git status` showed it untouched, so the session left it alone and edited only `lease.py`.
