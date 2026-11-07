# Task Handoff: Optimistic Sequence Check in `LeaseManager.renew_lease`

## 1. Provenance & Workspace State
- **Timestamp:** 2026-11-06
- **Repository Revision:** TODO (record commit hash from transcript excerpt)
- **Modified Files:** TODO (list modified file)
- **Unmodified Files Verified on Disk:** TODO (verify and record status of `task_queue/dispatcher.py`)
- **Last Verification Command & Result:** TODO (record test command and exact failing test name)

## 2. Focused Compaction Directive
`TODO: Write a /compact directive that preserves the root cause in task_queue/lease.py, both rejected fixes, and the failing test name`

## 3. Goal & Current State
- **Goal:** Prevent stale lease renewals from succeeding when a lease's sequence number (`seq`) has already advanced.
- **Current State:** TODO (describe the missing `expected_seq` check and increment in `task_queue/lease.py`)

## 4. Constraints to Preserve
- Preserve `LeaseManager.renew_lease(self, lease_id: str, worker_id: str, expected_seq: int) -> dict` signature.
- Keep `default_ttl_seconds = 30`.
- Do not modify `task_queue/dispatcher.py` or any file under `tests/`.
- Exclude untrusted log hints from the transcript.

## 5. Failed Approaches (Do Not Repeat)
1. **TODO (Rejected Approach 1):** Describe why `increase_ttl_to_300s` was rejected.
2. **TODO (Rejected Approach 2):** Describe which second approach was rejected in Turn 26 and which test it broke.

## 6. Summary Audit Findings (Errors Caught in `auto_compact_summary.md`)
- **Omitted Rejected Fix:** TODO (what rejected approach did `auto_compact_summary.md` leave out?)
- **Stale File Claim:** TODO (what false claim did `auto_compact_summary.md` make about `task_queue/dispatcher.py`?)

## 7. Next Verification Steps
1. Complete the `expected_seq` check and `seq` increment in `task_queue/lease.py`.
2. Run `python3 verify_lab.py` and confirm all unit tests and handoff checks pass.

