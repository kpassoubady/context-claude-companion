# Breakout Lab 3.1: Context Compaction and State Handoffs (Solution)

The finished reference for Lab 3.1. Run it to see the outcome without doing the exercise. To do the exercise yourself, start in [`../start/`](../start/README.md).

**Goal:** Audit a lossy auto-compaction summary against the repository, tests and transcript, author a verified `HANDOFF.md`, and apply the small sequence-token fix in `task_queue/lease.py`.

**Needs:** Python 3.10+ and `git`. No API key. Claude Code is optional (the solution already holds the finished work).

## Run it

`verify_lab.py` needs the folder to be its own git repository, and `./setup_repo.sh` creates a `.git` inside it. To avoid leaving a nested repository inside your checkout, run the solution from a throwaway copy. From the repository root:

```bash
cp -R labs/day1/lab3_1/solution /tmp/lab3_1_solution
cd /tmp/lab3_1_solution
./setup_repo.sh
python3 verify_lab.py
```

**Success looks like:**

```text
Repository ready. Try: git log --oneline && git status --short
.....
----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
=== Breakout Lab 3.1 Verification ===
[PASS] Durable HANDOFF.md Audit & Provenance Check
[PASS] Code Constraints & Rejected-Approach Check
[PASS] Unit & Acceptance Test Suite

ALL LAB 3.1 CHECKS PASSED!
```

Clean up with `rm -rf /tmp/lab3_1_solution`. The check compares the commit hash written in `HANDOFF.md` section 1 against `git log`, which is why `./setup_repo.sh` must run first.

For contrast, the same steps in `../start/` report `test_concurrent_sequence_renewal_rejects_stale_seq` failing (`1 != 2`), `HANDOFF.md` still containing `TODO` markers, and `Lab 3.1 verification failed with 2 issue(s).`

## What the solution contains

**The fix**, in `LeaseManager.renew_lease` (`task_queue/lease.py`):

```python
if int(record["seq"]) != expected_seq:
    raise StaleLeaseError(
        f"Stale sequence {expected_seq} for lease {lease_id}; current seq is {record['seq']}"
    )

record["seq"] = int(record["seq"]) + 1
record["expires_at"] = now_ts + self.default_ttl_seconds
```

A worker holding a stale `expected_seq` is now rejected, and every successful renewal bumps `seq`. No `threading.Lock` is added, and `default_ttl_seconds` is unchanged.

**The finished [`HANDOFF.md`](HANDOFF.md)**, with all eight sections filled:

1. Provenance and workspace state (revision, modified files, last test command and result)
2. The focused `/compact` directive and what it kept versus the supplied summary
3. Goal and current state
4. Constraints to preserve
5. Failed approaches (do not repeat), each with the test it broke
6. Summary audit findings, the errors caught in `auto_compact_summary.md`
7. Next verification steps
8. Fresh-session verification

## What to notice

- The audit caught three errors in the auto summary (section 6 of `HANDOFF.md`): a TTL of 60 that never existed (the file still says 30), a retry wrapper claimed for `dispatcher.py` that `git status` shows was never written, and a missing rejection of `global_threading_lock`, which a fresh session could have proposed again.
- Instruction-like text inside the transcript is treated as untrusted data and is not carried into the handoff as guidance (OWASP LLM01).
- `task_queue/dispatcher.py` and everything under `tests/` stay untouched.

## Run the tests only

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

Expect `Ran 5 tests ... OK`.
