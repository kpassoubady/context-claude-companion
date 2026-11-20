"""
Demo - Context Lifecycle Inspector
Day 1 - Topic 2

Goal: Parse `.claude/rules/*.md` YAML frontmatter globs and demonstrate which instructions load at session startup versus on demand when Claude Code accesses specific repository files.

This script implements a real frontmatter parser and glob matcher modeled on Claude Code's context lifecycle, comparing a 320-line monolithic `CLAUDE.md` against a concise root `CLAUDE.md` paired with path-scoped `.claude/rules/*.md` files. Sizes are labeled estimates; verify live behavior with `/context`.

No API key needed. Pure Python.

Run: python3 day1/demos/demo-context-lifecycle-inspector.py
"""

from fnmatch import fnmatch

MONOLITHIC_CLAUDE_MD_LINES = 320
CONCISE_ROOT_CLAUDE_MD = """# Order & Fulfillment Monorepo
- Import shared agent notes: @AGENTS.md
- Run all unit tests: pytest -q
- Keep monetary values in integer cents across services.
"""

RULE_FILES = {
    ".claude/rules/global-security.md": """# Global Security Hygiene
- Never commit API keys, tokens, or customer PII to repository files.
""",
    ".claude/rules/orders-service.md": """---
paths:
  - "services/orders/**/*.py"
  - "tests/orders/**/*.py"
---
# Orders Service Rules
- Represent all prices and discounts in integer cents; never use float.
- Require idempotency_key on all order mutation functions.
- Verify with: pytest tests/orders -q
""",
    ".claude/rules/webhook-gateway.md": """---
paths:
  - "services/webhook_gateway/**/*.py"
---
# Webhook Gateway Rules
- Verify HMAC-SHA256 signatures before parsing webhook payloads.
- Use exponential backoff with jitter for outbound retries.
""",
}


def parse_rule_frontmatter(markdown_text: str) -> tuple[list[str], str]:
    """Extract `paths:` globs from YAML frontmatter if present."""
    lines = markdown_text.strip().splitlines()
    if not lines or lines[0].strip() != "---":
        return [], markdown_text.strip()

    paths: list[str] = []
    end_idx = 0
    in_paths = False
    for idx in range(1, len(lines)):
        line = lines[idx].strip()
        if line == "---":
            end_idx = idx
            break
        if line.startswith("paths:"):
            in_paths = True
            continue
        if in_paths and line.startswith("-"):
            glob_val = line.lstrip("-").strip().strip('"').strip("'")
            paths.append(glob_val)

    body = "\n".join(lines[end_idx + 1 :]).strip()
    return paths, body


def matches_any_glob(target_path: str, globs: list[str]) -> bool:
    """Match a repository file path against Claude Code rule globs."""
    for pattern in globs:
        normalized = pattern.replace("**/", "")
        if fnmatch(target_path, pattern) or fnmatch(target_path, normalized):
            return True
    return False


def resolve_loaded_guidance(accessed_files: list[str]) -> list[tuple[str, str, int]]:
    """Return (source, trigger_reason, line_count) for a given session state."""
    loaded = [("CLAUDE.md (root)", "startup", len(CONCISE_ROOT_CLAUDE_MD.strip().splitlines()))]

    for rule_path, raw_content in RULE_FILES.items():
        globs, body = parse_rule_frontmatter(raw_content)
        line_count = len(body.splitlines())
        if not globs:
            loaded.append((rule_path, "startup (no paths: frontmatter)", line_count))
        else:
            matched_files = [f for f in accessed_files if matches_any_glob(f, globs)]
            if matched_files:
                loaded.append((rule_path, f"on-demand (matched {matched_files[0]})", line_count))
    return loaded


def main() -> None:
    scenarios = [
        ("1. Session Startup (before file reads)", []),
        ("2. Reading services/orders/pricing.py", ["services/orders/pricing.py"]),
        ("3. Control: Reading scripts/legacy_migration/run.py", ["scripts/legacy_migration/run.py"]),
    ]

    print(f"Baseline comparison: Monolithic root CLAUDE.md loads {MONOLITHIC_CLAUDE_MD_LINES} lines at startup on every session.\n")

    for title, files in scenarios:
        print(f"=== {title} ===")
        loaded = resolve_loaded_guidance(files)
        total_lines = 0
        for source, reason, count in loaded:
            total_lines += count
            print(f"  + {source:<36} | {reason:<42} | {count:>2} lines")
        print(f"  Total guidance lines in active window: {total_lines} lines\n")

    print(
        "Takeaway: Root CLAUDE.md and unconditional rules load at startup, while `.claude/rules/` "
        "files with `paths:` globs load on demand only when matching files are accessed."
    )


if __name__ == "__main__":
    main()

