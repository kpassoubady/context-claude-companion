"""Deterministic acceptance check for Breakout Lab 2.1."""

import ast
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent


def check_root_claude_md() -> list[str]:
    errors = []
    claude_md = ROOT / "CLAUDE.md"
    if not claude_md.exists():
        return ["CLAUDE.md is missing."]
    text = claude_md.read_text(encoding="utf-8")
    lines = text.strip().splitlines()
    if len(lines) > 60:
        errors.append(f"CLAUDE.md has {len(lines)} lines (must be <= 60 lines).")
    if "@AGENTS.md" not in text:
        errors.append("CLAUDE.md must retain the explicit `@AGENTS.md` import.")
    if "verify_lab.py" not in text:
        errors.append("CLAUDE.md must include the `verify_lab.py` verification command.")
    if "LEGACY_FLOAT_DISCOUNT_RULE" in text or "use float(subtotal_cents)" in text:
        errors.append("CLAUDE.md still contains legacy float discount instructions.")
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
    if not lines or lines[0].strip() != "---":
        errors.append(".claude/rules/orders.md must begin with YAML frontmatter `---` on line 1.")
    else:
        end_idx = None
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                end_idx = idx
                break
        if end_idx is None:
            errors.append(".claude/rules/orders.md YAML frontmatter is missing closing `---`.")
        else:
            frontmatter = "\n".join(lines[1:end_idx])
            if "paths:" not in frontmatter:
                errors.append(".claude/rules/orders.md frontmatter is missing `paths:`.")
            if "services/orders/" not in frontmatter or "tests/orders/" not in frontmatter:
                errors.append(".claude/rules/orders.md `paths:` must scope both `services/orders/**` and `tests/orders/**`.")
    if "idempotency_key" not in text or "int" not in text.lower():
        errors.append(".claude/rules/orders.md must document the integer cents and `idempotency_key` invariants.")
    return errors


def check_pricing_implementation() -> list[str]:
    errors = []
    pricing_path = ROOT / "services" / "orders" / "pricing.py"
    source = pricing_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == "float":
            errors.append("services/orders/pricing.py still references `float` in executable AST.")
    return errors


def check_comparison_record() -> list[str]:
    comp_path = ROOT / "context_comparison.md"
    if not comp_path.exists():
        return ["context_comparison.md is missing."]
    text = comp_path.read_text(encoding="utf-8")
    if "| TODO" in text or ": TODO" in text:
        return ["context_comparison.md still contains unfilled `TODO` placeholders."]
    return []


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
