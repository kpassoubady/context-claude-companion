"""
Demo - Context Hazard Linter
Day 1 - Topic 4

Goal: Audit a repository's context files for stale paths, conflicting directives, unscoped rules, duplicate lines, and verbose tool output.

This script reads the real files in `fixtures/hazard_repo/` (`CLAUDE.md`, `.claude/rules/*.md`, and a captured tool log), checks every backticked path against the file system with `Path.exists()`, derives conflicts by pairing "forbidden" tools in one file with recommendations in another, and counts lines in the log file. Change a fixture file and rerun to see the report change. Static checks do not replace human review or tests.

No API key needed. Python 3 standard library only.

Run (from the companion repo root): python3 day1/demos/demo-context-hazard-linter.py
"""

import re
from pathlib import Path

REPO = Path(__file__).parent / "fixtures" / "hazard_repo"
LOG_LINE_LIMIT = 500


def instruction_files() -> dict[str, str]:
    files = {"CLAUDE.md": (REPO / "CLAUDE.md").read_text()}
    for p in sorted((REPO / ".claude" / "rules").glob("*.md")):
        files[str(p.relative_to(REPO))] = p.read_text()
    return files


def detect_stale_paths(files: dict[str, str]) -> list[tuple[str, str]]:
    """Backticked paths in instructions that do not exist in the repo."""
    stale = []
    for name, text in files.items():
        for candidate in re.findall(r"`([\w./-]+\.\w+)`", text):
            if "/" in candidate and not (REPO / candidate).exists():
                stale.append((name, candidate))
    return stale


FORBIDDEN = re.compile(r"never use\s+`?(\w+)`?|`(\w+)` is forbidden", re.I)
TOOL_ALIASES = {"unittest": ["unittest"], "requests": ["requests"]}


def detect_conflicts(files: dict[str, str]) -> list[str]:
    """A tool one file forbids that another file tells Claude to use."""
    conflicts = []
    for src, text in files.items():
        forbidden = {m for g in FORBIDDEN.findall(text) for m in g if m} & set(TOOL_ALIASES)
        for tool in forbidden:
            for other, other_text in files.items():
                if other == src:
                    continue
                for line in other_text.splitlines():
                    if re.search(rf"\b{tool}\b", line) and re.search(r"\b(use|run)\b", line, re.I):
                        conflicts.append(f"`{tool}` is forbidden in {src} but {other} says: {line.strip('- ').strip()}")
    return conflicts


def detect_unscoped_rules(files: dict[str, str]) -> list[str]:
    return [n for n, t in files.items() if n.startswith(".claude/rules/") and not t.lstrip().startswith("---")]


def detect_duplicates(files: dict[str, str]) -> list[tuple[str, str]]:
    dups = []
    for name, text in files.items():
        seen = set()
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("- "):
                if line in seen:
                    dups.append((name, line))
                seen.add(line)
    return dups


def main() -> None:
    files = instruction_files()
    print(f"=== Context Hazard Audit of fixtures/hazard_repo ({len(files)} instruction files) ===\n")

    stale = detect_stale_paths(files)
    print(f"1. Stale path references ({len(stale)} found):")
    for name, path in stale:
        print(f"   - {name}: `{path}` does not exist on disk")

    conflicts = detect_conflicts(files)
    print(f"\n2. Conflicting directives ({len(conflicts)} found):")
    for c in conflicts:
        print(f"   - {c}")

    unscoped = detect_unscoped_rules(files)
    print(f"\n3. Rules without `paths:` frontmatter ({len(unscoped)} found):")
    for name in unscoped:
        print(f"   - {name} loads on every session start")

    dups = detect_duplicates(files)
    print(f"\n4. Duplicate lines ({len(dups)} found):")
    for name, line in dups:
        print(f"   - {name}: {line}")

    log = REPO / "logs" / "last_tool_output.txt"
    n = len(log.read_text().splitlines())
    print("\n5. Verbose tool output:")
    status = "over the limit; bound with `-q --tb=short` or path filters" if n > LOG_LINE_LIMIT else "within the limit"
    print(f"   - {log.relative_to(REPO)} has {n:,d} lines ({status}, limit {LOG_LINE_LIMIT})")

    print(
        "\nTakeaway: Static checks catch broken paths, unscoped rules, and explicit contradictions "
        "so human review and tests can focus on whether Claude actually follows the guidance."
    )


if __name__ == "__main__":
    main()
