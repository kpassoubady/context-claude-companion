"""
Demo - Context Lifecycle Inspector
Day 1 - Topic 2

Goal: Show which instruction files load at session startup and which load on demand when a file matching a rule's `paths:` globs is accessed.

This script reads the real `CLAUDE.md` and `.claude/rules/*.md` files in `fixtures/rules_repo/`, parses their `paths:` frontmatter, and checks accessed files (which must exist on disk) against the globs. It also totals what the same guidance costs if every rule is inlined into one monolithic `CLAUDE.md`. The matcher is a small stand-in written for this demo, not Claude Code's own; verify live loading with `/context`. Edit a rule file in the fixture and rerun to see the output change.

No API key needed. Python 3 standard library only.

Run (from the companion repo root): python3 day1/demos/demo-context-lifecycle-inspector.py
"""

import re
from pathlib import Path

REPO = Path(__file__).parent / "fixtures" / "rules_repo"


def parse_rule(text: str) -> tuple[list[str], str]:
    """Return (`paths:` globs, body) for a rule file."""
    lines = text.strip().splitlines()
    if not lines or lines[0].strip() != "---":
        return [], text.strip()
    globs: list[str] = []
    end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    for line in lines[1:end]:
        if line.strip().startswith("-"):
            globs.append(line.strip().lstrip("-").strip().strip('"').strip("'"))
    return globs, "\n".join(lines[end + 1:]).strip()


def glob_to_regex(glob: str) -> re.Pattern:
    """`**/` spans directories, `*` stays inside one path segment."""
    out, i = "", 0
    while i < len(glob):
        if glob.startswith("**/", i):
            out += "(?:.*/)?"
            i += 3
        elif glob[i] == "*":
            out += "[^/]*"
            i += 1
        else:
            out += re.escape(glob[i])
            i += 1
    return re.compile(out + r"\Z")


def matches(path: str, globs: list[str]) -> bool:
    return any(glob_to_regex(g).match(path) for g in globs)


def load_rules() -> dict[str, tuple[list[str], str]]:
    return {
        str(p.relative_to(REPO)): parse_rule(p.read_text())
        for p in sorted((REPO / ".claude" / "rules").glob("*.md"))
    }


def resolve(accessed: list[str], rules: dict, root_lines: int) -> list[tuple[str, str, int]]:
    loaded = [("CLAUDE.md (root)", "startup", root_lines)]
    for name, (globs, body) in rules.items():
        n = len(body.splitlines())
        if not globs:
            loaded.append((name, "startup (no paths: frontmatter)", n))
            continue
        hit = next((f for f in accessed if matches(f, globs)), None)
        if hit:
            loaded.append((name, f"on-demand (matched {hit})", n))
    return loaded


def main() -> None:
    rules = load_rules()
    root_lines = len((REPO / "CLAUDE.md").read_text().strip().splitlines())
    monolith = root_lines + sum(len(body.splitlines()) for _, body in rules.values())
    print(f"Baseline: inlining every rule into one CLAUDE.md loads {monolith} lines at startup on every session.\n")

    scenarios = [
        ("1. Session startup (before file reads)", []),
        ("2. Reading services/orders/pricing.py", ["services/orders/pricing.py"]),
        ("3. Control: reading scripts/legacy_migration/run.py", ["scripts/legacy_migration/run.py"]),
    ]
    for title, files in scenarios:
        missing = [f for f in files if not (REPO / f).exists()]
        assert not missing, f"fixture file not found: {missing}"
        print(f"=== {title} ===")
        total = 0
        for source, reason, count in resolve(files, rules, root_lines):
            total += count
            print(f"  + {source:<38} | {reason:<52} | {count:>2} lines")
        print(f"  Guidance lines in the active window: {total} of {monolith}\n")

    print(
        "Takeaway: The root CLAUDE.md and rules without `paths:` load at startup; rules with `paths:` "
        "load only when a matching file is accessed."
    )


if __name__ == "__main__":
    main()
