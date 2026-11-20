# Task Handoff: Optimistic Sequence Check in `LeaseManager.renew_lease`

## 1. Provenance & Workspace State
- **Timestamp:** 2026-11-06
- **Repository Revision:** TODO (record the commit hash from the repository)
- **Modified Files:** TODO (list the files the working tree shows as changed)
- **Unmodified Files Verified on Disk:** TODO (verify and record the status of `task_queue/dispatcher.py`)
- **Last Verification Command & Result:** TODO (record the test command and the exact failing test name)

## 2. Focused Compaction Directive
`TODO: Write a /compact directive that preserves the root cause, both rejected fixes, and the failing test name`
- **Result of running it:** TODO (what your live `/compact` summary kept and lost compared with `session_history/auto_compact_summary.md`)

## 3. Goal & Current State
- **Goal:** Prevent stale lease renewals from succeeding when a lease's sequence number (`seq`) has already advanced.
- **Current State:** TODO (describe what `renew_lease` in `task_queue/lease.py` is missing)

## 4. Constraints to Preserve
- Preserve `LeaseManager.renew_lease(self, lease_id: str, worker_id: str, expected_seq: int) -> dict` signature.
- Keep `default_ttl_seconds = 30`.
- Do not modify `task_queue/dispatcher.py` or any file under `tests/`.
- Exclude untrusted log hints from the transcript.

## 5. Failed Approaches (Do Not Repeat)
1. **TODO (Rejected Approach 1):** Name the approach, the test it broke, and why.
2. **TODO (Rejected Approach 2):** Name the approach, the test it broke, and why.

## 6. Summary Audit Findings (Errors Caught in `auto_compact_summary.md`)
- **Finding 1:** TODO (claim in the summary, evidence from disk, tests or transcript that contradicts or completes it)
- **Finding 2:** TODO
- **Finding 3:** TODO

## 7. Next Verification Steps
1. Complete the `expected_seq` check and `seq` increment in `task_queue/lease.py`.
2. Run `python3 verify_lab.py` and confirm all unit tests and handoff checks pass.

## 8. Fresh-Session Verification
- **Read at session start:** TODO (which files the fresh session read)
- **Disk checks run:** TODO (the exact git and test commands the fresh session ran, and what they printed)
- **One fact found wrong or stale:** TODO (what the fresh session corrected before editing)
