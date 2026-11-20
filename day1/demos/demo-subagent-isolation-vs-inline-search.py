"""
Demo - Subagent Isolation vs. Inline Search
Day 1 - Topic 3

Goal: Measure what lands in the parent context window for a targeted inline search, a broad inline exploration, and the same broad exploration delegated to a subagent, then check when local `grep` beats an external index.

This script builds a 12-module service tree and a git repo in a temporary directory and runs the real `grep` and `cat` commands an agent would run. Token counts are measured from that real output (characters divided by 4). The subagent row models information flow: the child window receives the same real tool output and the parent receives only a report built from the real matches. No Claude Code subagent is launched here; see the live prompt printed at the end.

No API key needed. Needs python3, git, grep.

Run (from the companion repo root): python3 day1/demos/demo-subagent-isolation-vs-inline-search.py
"""

import subprocess
import tempfile
from pathlib import Path

SYMBOL = "verify_idempotency_token"
DEFINERS = (4, 9)
CALLERS = (2, 7, 11)
MENTIONERS = (1, 3, 5, 6, 8, 10, 12)  # modules whose docstrings mention idempotency


def build_tree(root: Path) -> None:
    for i in range(1, 13):
        body = [f'"""Module {i:02d} request handler."""']
        if i in MENTIONERS:
            body[0] = f'"""Module {i:02d} request handler. Callers should be idempotent."""'
        body += [f"def helper_{i}_{j}(ctx):\n    return ctx" for j in range(35)]
        if i in DEFINERS:
            body.append(f'def {SYMBOL}(req):\n    """Check the idempotency key."""\n    return req.headers.get("X-Idempotency-Key")')
        if i in CALLERS:
            body.append(f"def handle_{i}(req):\n    return {SYMBOL}(req)")
        path = root / f"services/mod_{i:02d}/handler.py"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n\n".join(body) + "\n")
    git = ["git", "-c", "user.name=demo", "-c", "user.email=demo@example.com"]
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(git + ["commit", "-qm", "baseline"], cwd=root, check=True)


def sh(root: Path, cmd: str) -> str:
    return subprocess.run(cmd, shell=True, cwd=root, capture_output=True, text=True).stdout


def est_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def targeted_inline(root: Path) -> tuple[int, list[str], list[str]]:
    """Grep for the symbol, then read only the files that define it."""
    hits = sh(root, f"grep -rn {SYMBOL} services")
    defs = sorted({l.split(":")[0] for l in hits.splitlines() if f"def {SYMBOL}" in l})
    tokens = est_tokens(hits) + sum(est_tokens(sh(root, f"cat {p}")) for p in defs)
    callers = sorted({l.split(":")[0] for l in hits.splitlines() if f"def {SYMBOL}" not in l})
    return tokens, defs, callers


def broad_exploration(root: Path) -> tuple[int, list[str], list[str]]:
    """Grep the broad topic, read every matching module in full, then grep the symbol."""
    topic_files = sh(root, "grep -rl idempotent services; grep -rl idempotency services").split()
    topic_files = sorted(set(topic_files))
    tokens = est_tokens("\n".join(topic_files))
    for p in topic_files:
        tokens += est_tokens(sh(root, f"cat {p}"))
    hits = sh(root, f"grep -rn {SYMBOL} services")
    tokens += est_tokens(hits)
    defs = sorted({l.split(":")[0] for l in hits.splitlines() if f"def {SYMBOL}" in l})
    callers = sorted({l.split(":")[0] for l in hits.splitlines() if f"def {SYMBOL}" not in l})
    return tokens, defs, callers


def local_hits(root: Path, pattern: str) -> int:
    return len(sh(root, f"grep -rn {pattern} . --include=*.py --include=*.md").splitlines())


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve() / "service_repo"
        root.mkdir()
        build_tree(root)

        t_tokens, defs, callers = targeted_inline(root)
        b_tokens, _, _ = broad_exploration(root)
        report = (
            f"`{SYMBOL}` is defined in {', '.join(defs)} and called from {', '.join(callers)}. "
            "Static scan only; run pytest on those modules to confirm runtime behavior."
        )
        r_tokens = est_tokens(report)

        print("=== 1. Parent context footprint (tokens measured from real grep/cat output) ===")
        print(f"{'Mode':<50} | {'Parent window':>13} | {'Subagent window':>15} | {'Total model work':>16}")
        print("-" * 104)
        rows = [
            ("A. Inline, targeted (grep symbol + read 2 files)", t_tokens, 0, t_tokens),
            ("B. Inline, broad (read every module that matches)", b_tokens, 0, b_tokens),
            ("C. Subagent, same broad exploration (modeled)", r_tokens, b_tokens, b_tokens + r_tokens),
        ]
        for name, parent, child, total in rows:
            print(f"{name:<50} | {parent:>13,d} | {child:>15,d} | {total:>16,d}")
        print(f"\nSubagent report returned to the parent ({r_tokens} tokens): {report}")
        print("Reading: a targeted grep is already cheap inline. Delegation pays off for the broad case B, and it still costs total tokens.")
        print("Governance: a subagent shares the local filesystem and credentials unless you sandbox it.")

        print("\n=== 2. Local grep vs. external index (checks run on the repo) ===")

        # Scenario 1: exact symbol lookup.
        n = local_hits(root, SYMBOL)
        print(f"  Task: callers of `{SYMBOL}` in this repo\n    grep hits: {n} -> local Grep + Read")

        # Scenario 2: uncommitted change vs. an index built before the edit.
        index = {str(p.relative_to(root)): p.read_text() for p in root.rglob("*.py")}  # snapshot at index time
        target = root / "services/mod_04/handler.py"
        target.write_text(target.read_text() + "\ndef verify_idempotency_token_v2(req):\n    return None\n")
        index_hits = sum(1 for text in index.values() if "verify_idempotency_token_v2" in text)
        grep_hits = local_hits(root, "verify_idempotency_token_v2")
        diff = sh(root, "git diff --stat").strip().splitlines()[-1]
        print("  Task: find an uncommitted edit made after the index was built")
        print(f"    index snapshot hits: {index_hits}; grep hits: {grep_hits}; git diff: {diff}")
        print("    -> working tree changes are visible to Grep and git diff, not to an index built earlier")

        # Scenario 3: external corpus.
        pm = local_hits(root, "-i postmortem")
        print("  Task: search 4,000 historical postmortems across 15 teams")
        print(f"    grep hits in this repo: {pm} -> corpus is not local; use an access-controlled retrieval service (not run here)")

    print(
        "\nLive pair: in Claude Code, ask 'Use a subagent to find where verify_idempotency_token is defined "
        "and called, and report only the file list', then compare `/context` before and after."
    )
    print(
        "Takeaway: Delegate broad exploratory reads to a subagent so the parent keeps a short report; use "
        "direct Grep and git for local code; reserve an external index for corpora that are not on disk."
    )


if __name__ == "__main__":
    main()
