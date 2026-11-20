"""
Demo - Multi-Turn Agent Loop Context Growth
Day 1 - Topic 1

Goal: Measure how the output of six agent tool calls accumulates in the context window when the calls are unbounded versus scoped to source files.

This script builds a small Python telemetry-ingest project in a temporary directory (`src/`, `tests/`, a compiled `dist/` bundle, and a vendored `node_modules/` package), initialises git, and runs the commands an agent would run: `ls`, `grep`, `cat`, `pytest`, and `git diff`. It counts the real lines and characters each command returns. Tokens are estimated as characters divided by 4. Verify the live window with `/context`.

No API key needed. Needs python3, pytest, git, grep. Standard library otherwise.

Run (from the companion repo root): python3 day1/demos/demo-agent-loop-context-growth.py
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def build_project(root: Path) -> None:
    files = {
        "CLAUDE.md": (
            "# Telemetry Worker\n"
            "- Edit Python sources in src/ only; never edit compiled files in dist/.\n"
            "- Run focused tests with: pytest tests/test_ingest.py -q\n"
        ),
        "pytest.ini": "[pytest]\npythonpath = .\n",
        "src/ingest/worker.py": "".join(
            f"def process_event_{i}(payload):\n    return payload.get('id')\n\n\n" for i in range(25)
        ),
        "src/ingest/validator.py": "".join(f"REQUIRED_FIELD_{i} = 'tenant_id'\n" for i in range(20)),
        "dist/ingest/worker.bundled.js": "".join(
            f"// compiled artifact line {i}: var process_event = function() {{}};\n" for i in range(400)
        ),
        "node_modules/vendor_pkg/index.js": "".join(
            f"// third-party vendor code line {i}{': process_event_wrapper' if i % 3 == 0 else ''}\n"
            for i in range(600)
        ),
        "tests/test_ingest.py": "from src.ingest import worker\n\n\n"
        + "".join(
            f"def test_case_{i}():\n    assert worker.process_event_{i % 25}({{'id': {i}}}) == {i}\n\n\n"
            for i in range(40)
        ),
    }
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    git = ["git", "-c", "user.name=demo", "-c", "user.email=demo@example.com"]
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(git + ["commit", "-qm", "baseline"], cwd=root, check=True)
    # The agent's actual edit, so `git diff` has real content.
    worker = root / "src/ingest/worker.py"
    worker.write_text(worker.read_text().replace("return payload.get('id')", "return payload.get('id') or ''", 1))


def run(root: Path, cmd: str) -> str:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONPATH="")
    proc = subprocess.run(cmd, shell=True, cwd=root, capture_output=True, text=True, env=env)
    # Normalise pytest's wall-clock time so repeated runs print identical numbers.
    return re.sub(r" in \d+\.\d+s", " in Ns", proc.stdout + proc.stderr)


PYTEST = f"{sys.executable} -m pytest -p no:cacheprovider"

UNBOUNDED = [
    ("cat CLAUDE.md", "cat CLAUDE.md"),
    ("ls -R (everything)", "ls -R"),
    ("grep -rn process_event . (whole repo)", "grep -rn process_event ."),
    ("cat dist/ingest/worker.bundled.js", "cat dist/ingest/worker.bundled.js"),
    ("pytest -vv (verbose dump)", f"{PYTEST} -vv"),
    ("re-read worker.py and dist bundle", "cat src/ingest/worker.py dist/ingest/worker.bundled.js"),
]

BOUNDED = [
    ("cat CLAUDE.md", "cat CLAUDE.md"),
    ("find src tests -type f", "find src tests -type f"),
    ("grep -rn -m5 process_event src/ingest", "grep -rn -m5 process_event src/ingest"),
    ("cat src/ingest/worker.py", "cat src/ingest/worker.py"),
    ("pytest tests/test_ingest.py -q", f"{PYTEST} tests/test_ingest.py -q"),
    ("git diff --stat src/", "git diff --stat src/"),
]


def polluted_lines(output: str) -> int:
    """Count output lines that came from build output (dist/) or vendored code (node_modules/)."""
    markers = ("./dist/", "./node_modules/", "compiled artifact line", "third-party vendor code")
    return sum(1 for line in output.splitlines() if any(m in line for m in markers))


def measure(root: Path, steps: list[tuple[str, str]]) -> list[dict]:
    total_chars = total_lines = 0
    rows = []
    for label, cmd in steps:
        out = run(root, cmd)
        lines, chars = len(out.splitlines()), len(out)
        total_lines += lines
        total_chars += chars
        rows.append({"label": label, "lines": lines, "cum_lines": total_lines,
                     "cum_tokens": total_chars // 4, "polluted": polluted_lines(out)})
    return rows


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve() / "telemetry_worker"
        root.mkdir()
        build_project(root)
        unbounded = measure(root, UNBOUNDED)
        bounded = measure(root, BOUNDED)

    print("=== Multi-Turn Agent Loop: real tool output per turn (cumulative) ===")
    print(f"{'Turn':<4} | {'Mode':<9} | {'Command':<40} | {'+Lines':>6} | {'Cum lines':>9} | {'Cum est tokens':>14} | Build/vendor lines")
    print("-" * 112)
    for i, (u, b) in enumerate(zip(unbounded, bounded), start=1):
        for mode, r in (("unbounded", u), ("bounded", b)):
            print(f"{i:<4} | {mode:<9} | {r['label']:<40} | {r['lines']:>6,d} | {r['cum_lines']:>9,d} | "
                  f"{r['cum_tokens']:>14,d} | {r['polluted']:>3d}")
        print()

    fu, fb = unbounded[-1], bounded[-1]
    pct = (1.0 - fb["cum_tokens"] / fu["cum_tokens"]) * 100.0
    print(f"After turn 6: unbounded {fu['cum_lines']:,d} lines / ~{fu['cum_tokens']:,d} tokens; "
          f"bounded {fb['cum_lines']:,d} lines / ~{fb['cum_tokens']:,d} tokens ({pct:.1f}% smaller).")
    print(
        "Takeaway: Each turn adds its tool output to the window and keeps it there. Scoping greps to src/, "
        "reading only the file you will edit, and using `pytest -q` kept build and vendor files out of every later turn."
    )


if __name__ == "__main__":
    main()
