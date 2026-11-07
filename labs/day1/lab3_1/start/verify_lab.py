"""Deterministic acceptance check for Breakout Lab 3.1."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent


def check_handoff_md() -> list[str]:
    errors = []
    handoff_path = ROOT / "HANDOFF.md"
    if not handoff_path.exists():
        return ["HANDOFF.md is missing."]
    text = handoff_path.read_text(encoding="utf-8")
    if "TODO" in text:
        errors.append("HANDOFF.md still contains unresolved `TODO` placeholders.")
    required_terms = [
        ("8f4a12c", "Provenance commit hash `8f4a12c`"),
        ("increase_ttl_to_300s", "Rejected approach 1 (`increase_ttl_to_300s`)"),
        ("global_threading_lock", "Rejected approach 2 (`global_threading_lock`)"),
        ("dispatcher.py", "Audit finding regarding unmodified `task_queue/dispatcher.py`"),
        ("test_concurrent_sequence_renewal_rejects_stale_seq", "Failing test name"),
        ("/compact", "Focused `/compact` directive"),
    ]
    for term, description in required_terms:
        if term not in text:
            errors.append(f"HANDOFF.md is missing required evidence: {description}.")
    if "delete test_concurrent_sequence_renewal_rejects_stale_seq" in text:
        errors.append("HANDOFF.md promoted an untrusted log instruction to delete tests.")
    return errors


def check_code_constraints() -> list[str]:
    errors = []
    lease_path = ROOT / "task_queue" / "lease.py"
    source = lease_path.read_text(encoding="utf-8")
    if "threading" in source or "Lock(" in source:
        errors.append("task_queue/lease.py used a rejected threading.Lock approach.")
    if "default_ttl_seconds: int = 30" not in source:
        errors.append("task_queue/lease.py changed default_ttl_seconds from 30.")

    dispatcher_path = ROOT / "task_queue" / "dispatcher.py"
    disp_source = dispatcher_path.read_text(encoding="utf-8")
    if "def validate_job_payload" not in disp_source or "retry" in disp_source.lower():
        errors.append("task_queue/dispatcher.py was modified contrary to project constraints.")
    return errors


def run_unit_tests() -> list[str]:
    sys.path.insert(0, str(ROOT))
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(ROOT / "tests"), pattern="test_*.py", top_level_dir=str(ROOT))
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    if result.testsRun < 4:
        return [f"Expected at least 4 unit tests to run, but ran {result.testsRun}."]
    if not result.wasSuccessful():
        return [f"Unit tests failed: {len(result.failures)} failure(s), {len(result.errors)} error(s)."]
    return []


def main() -> int:
    all_errors: list[str] = []
    checks = [
        ("Durable HANDOFF.md Audit & Provenance Check", check_handoff_md),
        ("Code Constraints & Rejected-Approach Check", check_code_constraints),
        ("Unit & Acceptance Test Suite", run_unit_tests),
    ]
    print("=== Breakout Lab 3.1 Verification ===")
    for label, fn in checks:
        errs = fn()
        if errs:
            print(f"[FAIL] {label}:")
            for e in errs:
                print(f"       - {e}")
            all_errors.extend(errs)
        else:
            print(f"[PASS] {label}")

    if all_errors:
        print(f"\nLab 3.1 verification failed with {len(all_errors)} issue(s).")
        return 1

    print("\nALL LAB 3.1 CHECKS PASSED!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

