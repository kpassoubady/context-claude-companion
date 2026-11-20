"""
Demo - Context Hazard Linter
Day 1 - Topic 4

Goal: Audit a repository's context configuration (`CLAUDE.md`, `.claude/rules/*.md`, and captured tool logs) to detect stale file paths, conflicting directives, unscoped subsystem rules, redundancy, and verbose tool dumps.

This script performs static checks against a sample repository fixture and reports actionable remediation steps while noting what still requires human review and runtime test verification.

No API key needed. Pure Python.

Run: python3 day1/demos/demo-context-hazard-linter.py
"""

import re

EXISTING_REPO_PATHS = {
    "services/api/client.py",
    "services/api/routes.py",
    "services/worker/jobs.py",
    "tests/api/test_client.py",
}

SAMPLE_CLAUDE_MD = """# Platform Service Repository
- Architecture docs live in `docs/legacy_v1/architecture.md` and `scripts/old_deploy.sh`.
- Standard testing: Run all tests using `python -m unittest discover`.
- Outbound HTTP: Use synchronous `requests.Session()` for service-to-service calls.
- Always write clean code, follow best practices, and be careful with errors.
- Always write clean code, follow best practices, and be careful with errors.
"""

SAMPLE_RULES = {
    ".claude/rules/api-async.md": """# FastAPI Service Rules (Missing paths: frontmatter!)
- Test runner: Always use `pytest tests/api -q` (never use unittest).
- Outbound HTTP: Always use `httpx.AsyncClient` for service-to-service calls; `requests` is forbidden.
""",
}

CAPTURED_TOOL_OUTPUT_LINES = 2400


def detect_stale_paths(markdown_text: str, valid_paths: set[str]) -> list[str]:
    """Find backticked file paths in instructions that do not exist in the repository."""
    candidates = re.findall(r"`([a-zA-Z0-9_./-]+\.[a-zA-Z0-9]+)`", markdown_text)
    return [p for p in candidates if "/" in p and p not in valid_paths]


def detect_conflicts(root_md: str, rules_map: dict[str, str]) -> list[str]:
    """Detect explicit contradictory tool/library directives across instruction files."""
    combined_rules = "\n".join(rules_map.values())
    conflicts = []
    if "unittest" in root_md and "never use unittest" in combined_rules:
        conflicts.append("Test runner conflict: root CLAUDE.md specifies `unittest`, but `.claude/rules/api-async.md` forbids `unittest` and requires `pytest`.")
    if "requests.Session()" in root_md and "`requests` is forbidden" in combined_rules:
        conflicts.append("HTTP client conflict: root CLAUDE.md recommends `requests.Session()`, but `.claude/rules/api-async.md` forbids `requests` in favor of `httpx.AsyncClient`.")
    return conflicts


def detect_unscoped_rules(rules_map: dict[str, str]) -> list[str]:
    """Flag component-specific `.claude/rules/*.md` files missing `paths:` frontmatter."""
    unscoped = []
    for path, content in rules_map.items():
        if not content.lstrip().startswith("---"):
            unscoped.append(f"{path} has no `paths:` YAML frontmatter (loads unconditionally on every session start).")
    return unscoped


def detect_duplicate_lines(markdown_text: str) -> list[str]:
    """Find duplicate bullet lines inside an instruction file."""
    seen = set()
    dups = []
    for line in markdown_text.splitlines():
        cleaned = line.strip()
        if cleaned.startswith("- "):
            if cleaned in seen:
                dups.append(cleaned)
            seen.add(cleaned)
    return dups


def main() -> None:
    print("=== Context Hazard Audit Report (Static Fixture Inspection) ===\n")

    stale = detect_stale_paths(SAMPLE_CLAUDE_MD, EXISTING_REPO_PATHS)
    print(f"1. Stale Path References ({len(stale)} found):")
    for item in stale:
        print(f"   - `{item}` does not exist in working tree")

    conflicts = detect_conflicts(SAMPLE_CLAUDE_MD, SAMPLE_RULES)
    print(f"\n2. Conflicting Directives ({len(conflicts)} found):")
    for item in conflicts:
        print(f"   - {item}")

    unscoped = detect_unscoped_rules(SAMPLE_RULES)
    print(f"\n3. Context Dilution / Unscoped Rules ({len(unscoped)} found):")
    for item in unscoped:
        print(f"   - {item}")

    dups = detect_duplicate_lines(SAMPLE_CLAUDE_MD)
    print(f"\n4. Redundant / Generic Instructions ({len(dups)} found):")
    for item in dups:
        print(f"   - Duplicate generic rule: {item}")

    print("\n5. Verbose Tool Output Check:")
    if CAPTURED_TOOL_OUTPUT_LINES > 500:
        print(f"   - Last tool output dumped {CAPTURED_TOOL_OUTPUT_LINES:,d} lines; bound with `-q --tb=short` or path filters.")

    print(
        "\nTakeaway: Static checks quickly catch broken paths, unscoped rule files, and explicit "
        "contradictions, freeing human reviewers and runtime tests to verify semantic adherence."
    )


if __name__ == "__main__":
    main()

