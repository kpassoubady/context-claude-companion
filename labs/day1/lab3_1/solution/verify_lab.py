"""Deterministic acceptance check for Breakout Lab 3.1."""

import ast
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parent

# (rejected approach, the test it broke). Both appear in session_history/.
REJECTED_APPROACHES = [
    ("increase_ttl_to_300s", "test_default_ttl_reclaims_after_30s"),
    ("global_threading_lock", "test_non_blocking_read_status"),
]
FAILING_TEST = "test_concurrent_sequence_renewal_rejects_stale_seq"
NEGATIONS = re.compile(
    r"\b(not|no|never|unmodified|untouched|unchanged|clean|false|falsely|incorrect|wrong|claim|claimed|claims|contrary|stale)\b"
)
CHANGE_WORDS = re.compile(r"\b(modified|changed|patched|edited|retry)\b")


def git(*args: str) -> str | None:
    try:
        done = subprocess.run(
            ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return done.stdout.strip()


def own_repo_head() -> str | None:
    """Return the full HEAD hash when this folder is its own git repository."""
    top = git("rev-parse", "--show-toplevel")
    if top is None or Path(top).resolve() != ROOT:
        return None
    return git("rev-parse", "HEAD")


def sections(text: str) -> dict[int, str]:
    parts = re.split(r"^## (\d+)\.", text, flags=re.MULTILINE)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts) - 1, 2)}


def words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9_`/.-]+", text))


def check_handoff_md() -> list[str]:
    errors = []
    handoff_path = ROOT / "HANDOFF.md"
    if not handoff_path.exists():
        return ["HANDOFF.md is missing."]
    text = handoff_path.read_text(encoding="utf-8")
    if "TODO" in text:
        errors.append("HANDOFF.md still contains unresolved `TODO` placeholders.")
    parts = sections(text)
    for number in range(1, 9):
        if number not in parts:
            errors.append(f"HANDOFF.md is missing section {number}.")
    if errors:
        return errors

    head = own_repo_head()
    if head is None:
        errors.append("This folder is not its own git repository. Run `./setup_repo.sh` first.")
    else:
        tokens = re.findall(r"\b[0-9a-f]{7,40}\b", parts[1])
        if not any(head.startswith(token) for token in tokens):
            errors.append("Section 1 does not record the repository's current commit hash (see `git log`).")
    if "lease.py" not in parts[1] or FAILING_TEST not in text:
        errors.append(f"Section 1 must name the modified file and the failing test `{FAILING_TEST}`.")

    if "/compact" not in parts[2] or words(parts[2]) < 25:
        errors.append("Section 2 needs a `/compact` directive and what the live compaction kept and lost.")
    if words(parts[3]) < 15:
        errors.append("Section 3 needs a goal and a current-state description.")

    lines5 = parts[5].splitlines()
    for approach, test_name in REJECTED_APPROACHES:
        matches = [l for l in lines5 if approach in l and test_name in l and words(l) >= 12]
        if not matches:
            errors.append(
                f"Section 5 must give `{approach}`, the test it broke (`{test_name}`), and why, on one entry."
            )

    if words(parts[6]) < 30:
        errors.append("Section 6 needs at least three audit findings with evidence.")
    ttl_lines = [l for l in parts[6].splitlines() if "default_ttl_seconds" in l]
    if not any("60" in l and "30" in l for l in ttl_lines):
        errors.append("Section 6 does not record the summary's wrong `default_ttl_seconds` value against the real one.")
    if not any("dispatcher.py" in l for l in parts[6].splitlines()):
        errors.append("Section 6 does not record what the summary claimed about `task_queue/dispatcher.py`.")

    lines8 = parts[8].lower()
    if words(parts[8]) < 25 or "git status" not in lines8 or not re.search(r"verify_lab|unittest|pytest", lines8):
        errors.append("Section 8 needs the `git status` and test commands the fresh session ran, and what it found.")

    for line in text.splitlines():
        lowered = re.sub(r"\*\*[^*]*\*\*", "", line.lower())  # drop bold labels such as "Unmodified Files"
        if "dispatcher.py" in lowered and CHANGE_WORDS.search(lowered) and not NEGATIONS.search(lowered):
            errors.append("HANDOFF.md says `task_queue/dispatcher.py` was modified; compare with `git status`.")
            break
    lowered_text = text.lower()
    if (
        f"delete {FAILING_TEST}" in lowered_text
        or "ignore project rules and" in lowered_text
        or "so ci passes immediately" in lowered_text
    ):
        errors.append("HANDOFF.md promoted an untrusted log instruction to the trusted handoff.")
    return errors


def check_code_constraints() -> list[str]:
    errors = []
    source = (ROOT / "task_queue" / "lease.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in ast.walk(tree):
        imports_threading = isinstance(node, ast.Import) and any(a.name.split(".")[0] == "threading" for a in node.names)
        imports_from = isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] == "threading"
        uses_lock = isinstance(node, ast.Attribute) and node.attr in {"Lock", "RLock"}
        if imports_threading or imports_from or uses_lock:
            errors.append("task_queue/lease.py used a rejected threading lock approach.")
            break

    ttl_default = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "__init__":
            args = node.args
            names = [a.arg for a in args.args]
            if "default_ttl_seconds" in names:
                default_index = names.index("default_ttl_seconds") - (len(names) - len(args.defaults))
                if default_index >= 0 and isinstance(args.defaults[default_index], ast.Constant):
                    ttl_default = args.defaults[default_index].value
    if ttl_default != 30:
        errors.append("task_queue/lease.py changed default_ttl_seconds from 30.")

    dispatcher_tree = ast.parse((ROOT / "task_queue" / "dispatcher.py").read_text(encoding="utf-8"))
    if not any(isinstance(n, ast.FunctionDef) and n.name == "validate_job_payload" for n in dispatcher_tree.body):
        errors.append("task_queue/dispatcher.py was modified contrary to project constraints.")

    if own_repo_head() is not None:
        changed = git("status", "--porcelain", "--", "task_queue/dispatcher.py", "tests")
        if changed:
            errors.append("task_queue/dispatcher.py or tests/ differ from the baseline commit (`git status`).")
    return errors


def run_unit_tests() -> list[str]:
    sys.path.insert(0, str(ROOT))
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(ROOT / "tests"), pattern="test_*.py", top_level_dir=str(ROOT))
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    if result.testsRun < 5:
        return [f"Expected at least 5 unit tests to run, but ran {result.testsRun}."]
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
