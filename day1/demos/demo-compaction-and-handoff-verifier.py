"""
Demo - Compaction and Handoff Verifier
Day 1 - Session 3

Goal: Audit an unfocused auto-compaction summary against a focused `/compact` summary and a structured `HANDOFF.md` by verifying claims against actual repository state and test execution.

This script inspects a simulated mid-debugging repository state for a task-queue lease bug, demonstrating how lossy summaries drop negative constraints (rejected fixes) or retain stale file claims, and how a deterministic verification step catches drift before code changes resume.

No API key needed. Pure Python.

Run: python3 day1/demos/demo-compaction-and-handoff-verifier.py
"""

ACTUAL_REPO_STATE = {
    "git_commit": "8f4a12c",
    "modified_files": ["task_queue/lease.py"],
    "unmodified_files": ["task_queue/dispatcher.py", "task_queue/config.py"],
    "failing_test": "tests/test_lease.py::test_concurrent_lease_renewal",
    "rejected_approaches": [
        "increase_ttl_to_300s (broke heartbeat timeout test)",
        "global_threading_lock (failed concurrency throughput SLA)",
    ],
    "required_constraint": "Preserve LeaseManager.renew(worker_id, lease_id,observed_seq) signature",
}

UNFOCUSED_AUTO_SUMMARY = """Session Summary:
Investigated duplicate job execution in the task queue worker. Looked at dispatcher.py, config.py, and lease.py.
Tried adjusting lease TTL and locking mechanisms. Next step: finish fixing lease renewal in dispatcher.py and lease.py.
"""

FOCUSED_COMPACT_SUMMARY = """Focused Summary (/compact preserve root cause in lease.py, rejected TTL and global lock fixes, and failing test):
- Root cause is non-atomic sequence comparison in task_queue/lease.py.
- Rejected fixes: (1) increase_ttl_to_300s, (2) global_threading_lock.
- Failing test: tests/test_lease.py::test_concurrent_lease_renewal.
- Note: task_queue/dispatcher.py was also edited earlier.
"""

STRUCTURED_HANDOFF_MD = """# Task Handoff: Atomic Lease Renewal
- Revision: 8f4a12c
- Modified Files: task_queue/lease.py
- Goal: Prevent duplicate job execution when two workers renew an expiring lease.
- Current State: Root cause isolated to sequence check in task_queue/lease.py.
- Constraints: Preserve LeaseManager.renew(worker_id, lease_id, observed_seq) signature.
- Failed Approaches:
  1. increase_ttl_to_300s (broke heartbeat timeout test)
  2. global_threading_lock (failed concurrency throughput SLA)
- Next Verification: pytest tests/test_lease.py::test_concurrent_lease_renewal -q
"""


def audit_state_record(label: str, text: str, repo_state: dict) -> dict:
    """Check whether a summary or handoff preserves critical facts and avoids stale claims."""
    preserves_failing_test = repo_state["failing_test"] in text
    preserved_rejections = sum(1 for r in repo_state["rejected_approaches"] if r.split()[0] in text)
    preserves_signature = "LeaseManager.renew" in text
    claims_dispatcher_modified = "dispatcher.py was also edited" in text or "fixing lease renewal in dispatcher.py" in text
    stale_claim_detected = claims_dispatcher_modified and "task_queue/dispatcher.py" in repo_state["unmodified_files"]

    return {
        "label": label,
        "preserves_failing_test": preserves_failing_test,
        "preserved_rejections": f"{preserved_rejections}/{len(repo_state['rejected_approaches'])}",
        "preserves_signature": preserves_signature,
        "stale_file_claim": stale_claim_detected,
    }


def main() -> None:
    records = [
        audit_state_record("1. Unfocused Auto-Compaction", UNFOCUSED_AUTO_SUMMARY, ACTUAL_REPO_STATE),
        audit_state_record("2. Focused /compact Summary", FOCUSED_COMPACT_SUMMARY, ACTUAL_REPO_STATE),
        audit_state_record("3. Verified HANDOFF.md", STRUCTURED_HANDOFF_MD, ACTUAL_REPO_STATE),
    ]

    print("=== Auditing Compaction Summaries & Handoff Notes Against Disk/Test State ===")
    print(
        f"{'Artifact':<30} | {'Failing Test?':<13} | {'Rejected Fixes':<14} | "
        f"{'Signature?':<10} | {'Stale Claim?'}"
    )
    print("-" * 88)
    for rec in records:
        print(
            f"{rec['label']:<30} | {str(rec['preserves_failing_test']):<13} | "
            f"{rec['preserved_rejections']:<14} | {str(rec['preserves_signature']):<10} | "
            f"{'YES (drift!)' if rec['stale_file_claim'] else 'No (clean)'}"
        )

    print(
        "\nTakeaway: Compaction summaries are lossy; pairing focused `/compact` or a structured "
        "`HANDOFF.md` with immediate verification against `git status` and `pytest` prevents "
        "repeating rejected fixes or acting on stale file assumptions."
    )


if __name__ == "__main__":
    main()

