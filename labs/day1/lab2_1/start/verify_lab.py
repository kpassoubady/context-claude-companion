"""Deterministic acceptance check for Breakout Lab 2.1.

Checks the context configuration itself (scope of the path rule, removal of
conflicting guidance, evidence record), not just the Python behavior.
"""

import ast
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parent

MAX_CLAUDE_MD_LINES = 60  # CLAUDE.md must have strictly fewer lines than this.
STARTER_CLAUDE_MD_LINES = 75  # `wc -l start/CLAUDE.md` before any edit.

# The rule must scope every orders source and test file, and nothing else.
MUST_MATCH = ("services/orders/pricing.py", "tests/orders/test_pricing.py")
MUST_NOT_MATCH = ("services/notifications/notifier.py", "scripts/legacy_migration/migrate.py")

# Conflicting guidance that must be gone from the root CLAUDE.md.
CONFLICTING_GUIDANCE = (
    "LEGACY_FLOAT_DISCOUNT_RULE",
    "float(subtotal_cents)",
    "nosetests",
    "skip `idempotency_key`",
    "skip idempotency",
    "never require `idempotency_key`",
    "never require idempotency_key",
)
REQUIRED_LAYOUT = ("services/orders", "services/notifications", "scripts/legacy_migration")


def count_lines(text: str) -> int:
    """Line count as `wc -l` reports it for a newline-terminated file."""
    return len(text.splitlines())


def glob_to_regex(glob: str) -> re.Pattern:
    """Translate a path glob: `**/` spans zero or more directories, `*` stays in one."""
    out, i = [], 0
    while i < len(glob):
        if glob.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif glob.startswith("**", i):
            out.append(".*")
            i += 2
        elif glob[i] == "*":
            out.append("[^/]*")
            i += 1
        elif glob[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(glob[i]))
            i += 1
    return re.compile("^" + "".join(out) + "$")


def parse_paths(frontmatter: str) -> list[str]:
    """Extract the `paths:` list (block or inline form) from YAML frontmatter."""
    lines = frontmatter.splitlines()
    for idx, line in enumerate(lines):
        if not re.match(r"^paths\s*:", line):
            continue
        inline = line.split(":", 1)[1].strip()
        if inline.startswith("["):
            items = inline.strip("[]").split(",")
        elif inline:
            items = [inline]
        else:
            items = []
            for follow in lines[idx + 1:]:
                m = re.match(r"^\s*-\s*(.+)$", follow)
                if not m:
                    break
                items.append(m.group(1))
        return [i.strip().strip("'\"") for i in items if i.strip().strip("'\"")]
    return []


def check_root_claude_md() -> list[str]:
    errors = []
    claude_md = ROOT / "CLAUDE.md"
    if not claude_md.exists():
        return ["CLAUDE.md is missing."]
    text = claude_md.read_text(encoding="utf-8")
    n = count_lines(text)
    if n >= MAX_CLAUDE_MD_LINES:
        errors.append(f"CLAUDE.md has {n} lines (must be under {MAX_CLAUDE_MD_LINES}).")
    if "@AGENTS.md" not in text:
        errors.append("CLAUDE.md must retain the explicit `@AGENTS.md` import.")
    if "verify_lab.py" not in text:
        errors.append("CLAUDE.md must include the `verify_lab.py` verification command.")
    missing = [p for p in REQUIRED_LAYOUT if p not in text]
    if missing:
        errors.append(f"CLAUDE.md must state the repository layout; missing: {', '.join(missing)}.")
    lowered = text.lower()
    found = [g for g in CONFLICTING_GUIDANCE if g.lower() in lowered]
    if found:
        errors.append(f"CLAUDE.md still contains conflicting guidance: {', '.join(found)}.")
    return errors


def check_scoped_orders_rule() -> list[str]:
    errors = []
    rule_path = ROOT / ".claude" / "rules" / "orders.md"
    if not rule_path.exists():
        return [".claude/rules/orders.md is missing."]
    text = rule_path.read_text(encoding="utf-8").strip()
    if "TODO" in text:
        errors.append(".claude/rules/orders.md still contains unresolved TODO placeholders.")
    lines = text.splitlines()
    body = text
    if not lines or lines[0].strip() != "---":
        errors.append(".claude/rules/orders.md must begin with YAML frontmatter `---` on line 1.")
    else:
        end_idx = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if end_idx is None:
            errors.append(".claude/rules/orders.md YAML frontmatter is missing closing `---`.")
        else:
            body = "\n".join(lines[end_idx + 1:])
            globs = parse_paths("\n".join(lines[1:end_idx]))
            if not globs:
                errors.append(".claude/rules/orders.md frontmatter needs a non-empty `paths:` list.")
            else:
                patterns = [glob_to_regex(g) for g in globs]
                for target in MUST_MATCH:
                    if not any(p.match(target) for p in patterns):
                        errors.append(f"`paths:` {globs} does not match {target}; the rule would not load for it.")
                for target in MUST_NOT_MATCH:
                    if any(p.match(target) for p in patterns):
                        errors.append(f"`paths:` {globs} also matches {target}; the rule is over-broad.")
    squashed = body.replace(" ", "").replace("_", "")
    if "idempotency_key" not in body or "ValueError" not in body:
        errors.append(".claude/rules/orders.md must state the `idempotency_key` / `ValueError` invariant.")
    if "float" not in body.lower() or "cents" not in body.lower():
        errors.append(".claude/rules/orders.md must state the integer-cents, never-`float` invariant.")
    if "5000)//10000" not in squashed:
        errors.append(".claude/rules/orders.md must state the integer half-up basis-point formula.")
    return errors


def check_pricing_implementation() -> list[str]:
    pricing_path = ROOT / "services" / "orders" / "pricing.py"
    tree = ast.parse(pricing_path.read_text(encoding="utf-8"))
    if any(isinstance(n, ast.Name) and n.id == "float" for n in ast.walk(tree)):
        return ["services/orders/pricing.py still references `float` in executable AST."]
    return []


PLACEHOLDERS = {"", "x", "xx", "tbd", "todo", "-", "--", "?", "..."}


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _real(value: str) -> bool:
    return value.strip("`* ").lower() not in PLACEHOLDERS and len(value.strip("`* ")) >= 3


def _field(text: str, label: str) -> str:
    m = re.search(rf"\*\*{re.escape(label)}[^*]*:\*\*[ \t]*(.*)", text)
    return m.group(1).strip() if m else ""


def check_comparison_record() -> list[str]:
    comp_path = ROOT / "context_comparison.md"
    if not comp_path.exists():
        return ["context_comparison.md is missing."]
    text = comp_path.read_text(encoding="utf-8")
    errors = []
    if re.search(r"\bTODO\b", text):
        return ["context_comparison.md still contains unfilled `TODO` placeholders."]

    prediction = _field(text, "Prediction")
    if len(prediction) < 20:
        errors.append("context_comparison.md needs your written prediction (at least a sentence).")
    if not re.fullmatch(r"(live|shared)\b.*", _field(text, "Observation Source").lower() or "-"):
        errors.append("context_comparison.md `Observation Source` must start with `live` or `shared`.")
    if not _real(_field(text, "Model / CLI Version")):
        errors.append("context_comparison.md needs the model / CLI version (or `N/A`).")

    rows = {}
    for line in text.splitlines():
        cells = _cells(line)
        if line.startswith("|") and len(cells) == 3 and cells[0].startswith("**"):
            rows[cells[0].lower()] = cells[1:]

    def row(key: str):
        return next((v for k, v in rows.items() if key in k), None)

    for key in ("line count", "paths:", "/context", "control read", "pricing tests", "adherence"):
        cells = row(key)
        if cells is None:
            errors.append(f"context_comparison.md is missing the `{key}` row.")
            continue
        for label, value in zip(("Before", "After"), cells):
            if not _real(value):
                errors.append(f"context_comparison.md `{key}` {label} cell is empty or a placeholder.")
        if key == "/context":
            for label, value in zip(("Before", "After"), cells):
                if value.strip("`* ").lower().startswith("n/a") or len(value) < 15:
                    errors.append(f"context_comparison.md `/context` {label} cell must hold the line(s) you observed.")

    lines_row = row("line count")
    if lines_row and all(_real(v) for v in lines_row):
        nums = [re.search(r"\d+", v) for v in lines_row]
        claude_md = ROOT / "CLAUDE.md"
        if nums[0] and int(nums[0].group()) != STARTER_CLAUDE_MD_LINES:
            errors.append(f"Before line count should be {STARTER_CLAUDE_MD_LINES} (`wc -l` of the starter CLAUDE.md).")
        if nums[1] and claude_md.exists() and int(nums[1].group()) != count_lines(claude_md.read_text(encoding="utf-8")):
            errors.append("After line count does not match `wc -l CLAUDE.md`.")
        if not all(nums):
            errors.append("Line count cells must contain a number.")

    globs_row = row("paths:")
    if globs_row and _real(globs_row[1]) and not ("orders" in globs_row[1]):
        errors.append("After `paths:` cell should list the globs you configured.")

    for label in ("Why the legacy comment", "Why `.claude/rules/` is not a security sandbox"):
        if len(_field(text, label)) < 30:
            errors.append(f"context_comparison.md judgment note `{label}` needs a real explanation.")
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
        ("Root CLAUDE.md Check", check_root_claude_md),
        ("Scoped .claude/rules/orders.md Check", check_scoped_orders_rule),
        ("AST Invariant Check (pricing.py)", check_pricing_implementation),
        ("Unit & Acceptance Test Suite", run_unit_tests),
        ("Before/After Comparison Record", check_comparison_record),
    ]
    print("=== Breakout Lab 2.1 Verification ===")
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
        print(f"\nLab 2.1 verification failed with {len(all_errors)} issue(s).")
        return 1

    print("\nALL LAB 2.1 CHECKS PASSED!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
