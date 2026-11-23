"""
Demo - Compaction and Handoff Verifier
Day 1 - Topic 3

Goal: Audit an unfocused auto-compaction summary, a focused `/compact` summary, and a `HANDOFF.md` against what `git status` and `pytest` report for the repository.

This script copies `fixtures/compaction_repo/` (a refund-ledger bug, separate from Lab 3.1) to a temporary directory, commits a baseline, applies one in-progress edit to `refunds/ledger.py`, then runs `git status --porcelain` and `pytest` to get the real modified files and the real failing test. It parses the method signature with `ast` and reads the rejected approaches from the session transcript. It then checks each summary file under `session_history/` against those facts.

No API key needed. Needs python3, pytest, git.

Run (from the companion repo root): python3 day1/demos/demo-compaction-and-handoff-verifier.py
"""

import ast
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FIXTURE = Path(__file__).parent / "fixtures" / "compaction_repo"
GIT = ["git", "-c", "user.name=demo", "-c", "user.email=demo@example.com"]


def sh(root: Path, cmd: list[str]) -> str:
    proc = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    return proc.stdout + proc.stderr


def build_session_state(root: Path) -> None:
    """Commit the fixture, then leave the working tree as it was mid-session."""
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(GIT + ["commit", "-qm", "baseline"], cwd=root, check=True)
    ledger = root / "refunds/ledger.py"
    ledger.write_text(ledger.read_text().replace(
        "        self._seen: set[str] = set()\n",
        "        self._seen: set[str] = set()\n        self._seen_at: dict[str, int] = {}  # WIP: first-seen order\n",
    ))


def collect_ground_truth(root: Path) -> dict:
    status = sh(root, ["git", "status", "--porcelain"]).rstrip().splitlines()
    modified = [line[3:] for line in status if not line.startswith("??")]
    pytest_out = sh(root, [sys.executable, "-m", "pytest", "-q", "-rf", "--tb=no", "--color=no", "-p", "no:cacheprovider"])
    failing = re.findall(r"^FAILED (\S+)", pytest_out, flags=re.M)

    tree = ast.parse((root / "refunds/ledger.py").read_text())
    func = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "post_refund")
    signature = f"post_refund({ast.unparse(func.args)}) -> {ast.unparse(func.returns)}"

    transcript = (root / "session_history/transcript_excerpt.md").read_text()
    rejected = re.findall(r"`(\w+)`[^\n]*REJECTED", transcript)

    return {"status": status, "modified": modified, "pytest_out": pytest_out,
            "failing": failing, "signature": signature, "rejected": rejected}


def audit(text: str, truth: dict) -> dict:
    """Check one summary against the facts that git, pytest, ast, and the transcript produced."""
    named_as_work = set()
    for line in text.splitlines():
        if re.search(r"edit|modif|fix|chang|updat", line, flags=re.I):
            named_as_work.update(re.findall(r"[\w/]+\.py", line))
    named_as_work = {p for p in named_as_work if not p.startswith("tests/")}
    return {
        "failing_test": all(f in text for f in truth["failing"]),
        "rejected": sum(1 for r in truth["rejected"] if r in text),
        "signature": truth["signature"] in text,
        "unmodified_named": sorted(named_as_work - set(truth["modified"])),
    }


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve() / "compaction_repo"
        shutil.copytree(FIXTURE, root)
        build_session_state(root)
        truth = collect_ground_truth(root)

        print("=== Ground truth from the repository ===")
        print(f"  git status --porcelain : {', '.join(l.strip() for l in truth['status']) or '(clean)'}")
        print(f"  pytest failing         : {', '.join(truth['failing']) or '(none)'}")
        print(f"  signature (ast)        : {truth['signature']}")
        print(f"  rejected (transcript)  : {', '.join(truth['rejected'])}")
        print()

        artifacts = [
            ("1. Unfocused auto-compaction", "auto_compact_summary.md"),
            ("2. Focused /compact summary", "focused_compact_summary.md"),
            ("3. HANDOFF.md", "HANDOFF.md"),
        ]
        print(f"{'Artifact':<30} | {'Failing test':<12} | {'Rejected fixes':<14} | {'Signature':<9} | Unmodified files named as work")
        print("-" * 110)
        for label, name in artifacts:
            r = audit((root / "session_history" / name).read_text(), truth)
            print(f"{label:<30} | {str(r['failing_test']):<12} | {f"{r['rejected']}/{len(truth['rejected'])}":<14} | "
                  f"{str(r['signature']):<9} | {', '.join(r['unmodified_named']) or 'none'}")

    print(
        "\nTakeaway: The automatic summary kept the story but dropped the failing test, both rejected fixes, "
        "and the signature, and it pointed the next step at a file git shows untouched. Check any summary or "
        "HANDOFF.md against `git status` and `pytest` before you resume work."
    )


if __name__ == "__main__":
    main()
