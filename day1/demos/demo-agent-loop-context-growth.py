"""
Demo - Multi-Turn Agent Loop Context Growth
Day 1 - Session 1

Goal: Simulate six turns of a Claude Code agent loop (`Gather -> Act -> Verify`) and measure how unbounded directory scans and build artifacts accumulate across turns compared to path-scoped queries.

This script executes real file-matching and line-filtering operations against an in-memory repository tree representing a SaaS telemetry ingestion pipeline (`src/`, `dist/`, `node_modules/`, `tests/`), comparing cumulative working-window growth across 6 turns.

No API key needed. Pure Python.

Run: python3 day1/demos/demo-agent-loop-context-growth.py
"""

from fnmatch import fnmatch

VIRTUAL_REPO_FILES = {
    "CLAUDE.md": "\n".join([
        "# Telemetry Worker",
        "- Edit TypeScript sources in src/ only; never edit compiled files in dist/.",
        "- Run focused tests with: pytest tests/test_ingest.py -q",
    ]),
    "src/ingest/worker.py": "\n".join([f"def process_event_{i}(payload): return payload.get('id')" for i in range(25)]),
    "src/ingest/validator.py": "\n".join([f"REQUIRED_FIELD_{i} = 'tenant_id'" for i in range(20)]),
    "dist/ingest/worker.bundled.js": "\n".join([f"// compiled artifact line {i}: var process_event = function() {{}};" for i in range(400)]),
    "node_modules/vendor_pkg/index.js": "\n".join([f"// third-party vendor code line {i}" for i in range(600)]),
    "tests/test_ingest.py": "\n".join([f"def test_case_{i}(): assert True" for i in range(40)]),
}

EXCLUDED_GLOBS = ("dist/**", "node_modules/**")


def is_excluded(path: str) -> bool:
    """Return True if path matches a build artifact or dependency directory."""
    return any(fnmatch(path, pat) for pat in EXCLUDED_GLOBS)


def run_unbounded_turn_sequence() -> list[tuple[int, str, int, list[str]]]:
    """Execute 6 agent turns without path filters or output bounds."""
    history_lines = 0
    records = []
    steps = [
        (1, "Load CLAUDE.md", ["CLAUDE.md"], 1.0),
        (2, "Broad file listing (all dirs)", list(VIRTUAL_REPO_FILES.keys()), 0.5),
        (3, "Unscoped grep across repo (includes dist/ & node_modules/)", list(VIRTUAL_REPO_FILES.keys()), 1.0),
        (4, "Read compiled artifact dist/ingest/worker.bundled.js", ["dist/ingest/worker.bundled.js"], 1.0),
        (5, "Verbose test suite dump (all tests -vv)", ["tests/test_ingest.py", "node_modules/vendor_pkg/index.js"], 1.0),
        (6, "Re-read src/ and dist/ after confusion", ["src/ingest/worker.py", "dist/ingest/worker.bundled.js"], 1.0),
    ]
    for turn, action, paths, factor in steps:
        added_lines = sum(int(len(VIRTUAL_REPO_FILES[p].splitlines()) * factor) for p in paths)
        history_lines += added_lines
        polluted = [p for p in paths if is_excluded(p)]
        records.append((turn, action, history_lines, polluted))
    return records


def run_bounded_turn_sequence() -> list[tuple[int, str, int, list[str]]]:
    """Execute 6 agent turns using targeted paths and concise tool outputs."""
    history_lines = 0
    records = []
    source_only = [p for p in VIRTUAL_REPO_FILES if not is_excluded(p)]
    steps = [
        (1, "Load CLAUDE.md", ["CLAUDE.md"], 1.0),
        (2, "Targeted Glob in src/ and tests/ only", source_only, 0.1),
        (3, "Scoped Grep in src/ingest/ (--max-count=5)", ["src/ingest/worker.py", "src/ingest/validator.py"], 0.25),
        (4, "Targeted Read of src/ingest/worker.py", ["src/ingest/worker.py"], 1.0),
        (5, "Focused test run (pytest tests/test_ingest.py -q)", ["tests/test_ingest.py"], 0.15),
        (6, "Verify clean diff on src/ingest/worker.py", ["src/ingest/worker.py"], 0.2),
    ]
    for turn, action, paths, factor in steps:
        added_lines = max(2, sum(int(len(VIRTUAL_REPO_FILES[p].splitlines()) * factor) for p in paths))
        history_lines += added_lines
        polluted = [p for p in paths if is_excluded(p)]
        records.append((turn, action, history_lines, polluted))
    return records


def main() -> None:
    unbounded = run_unbounded_turn_sequence()
    bounded = run_bounded_turn_sequence()

    print("=== Multi-Turn Agent Loop Context Accumulation (6 Turns) ===")
    print(f"{'Turn':<4} | {'Unbounded Lines':>15} | {'Bounded Lines':>13} | {'Bounded Action & Pollution Check'}")
    print("-" * 88)
    for (t1, act_u, lines_u, pol_u), (t2, act_b, lines_b, pol_b) in zip(unbounded, bounded):
        pol_note = f" [Unbounded read {', '.join(pol_u)}]" if pol_u else ""
        print(f"{t1:<4} | {lines_u:>15,d} | {lines_b:>13,d} | {act_b}{pol_note}")

    final_u = unbounded[-1][2]
    final_b = bounded[-1][2]
    reduction_pct = (1.0 - (final_b / final_u)) * 100.0
    print(f"\nCumulative context lines after Turn 6: Unbounded={final_u:,d} vs. Bounded={final_b:,d} ({reduction_pct:.1f}% smaller)")
    print(
        "Takeaway: Each turn in an agentic loop compounds context; scoping searches to source "
        "directories and bounding test output prevents build artifacts and logs from polluting later turns."
    )


if __name__ == "__main__":
    main()

