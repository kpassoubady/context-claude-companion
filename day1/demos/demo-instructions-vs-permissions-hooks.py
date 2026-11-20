"""
Demo - Instructions vs. Permissions and Hooks
Day 1 - Topic 2

Goal: Contrast advisory model-facing instructions (`CLAUDE.md`) with deterministic pre-action permission/hook gates (`PreToolUse`) and post-action verification checks (`PostToolUse`).

This script evaluates simulated tool invocations against a repository policy configuration, demonstrating why `CLAUDE.md` guides coding choices while permissions and `PreToolUse` hooks block disallowed tool calls before execution, and why `PostToolUse` runs after an action has already taken place.

No API key needed. Pure Python.

Run: python3 day1/demos/demo-instructions-vs-permissions-hooks.py
"""

from fnmatch import fnmatch

ADVISORY_CLAUDE_MD_RULES = [
    "Use integer cents for monetary fields in services/orders/.",
    "Do not edit locked migration files under migrations/locked/.",
]

PERMISSION_DENY_PATTERNS = [
    "Bash(rm -rf *)",
    "Edit(migrations/locked/**)",
]


def evaluate_pre_tool_use(tool_name: str, target_arg: str) -> tuple[bool, str]:
    """Deterministic PreToolUse and permission gate executed BEFORE the tool runs."""
    call_signature = f"{tool_name}({target_arg})"
    for pattern in PERMISSION_DENY_PATTERNS:
        normalized = pattern.replace("**", "*")
        if fnmatch(call_signature, pattern) or fnmatch(call_signature, normalized):
            return False, f"BLOCKED before execution by permission/PreToolUse rule: {pattern}"
    return True, "ALLOWED by PreToolUse gate"


def evaluate_post_tool_use(tool_name: str, target_arg: str, file_content: str) -> str:
    """PostToolUse check executed AFTER a write/edit has already completed."""
    if tool_name in ("Edit", "Write") and target_arg.endswith(".py"):
        if "float(" in file_content:
            return "PostToolUse lint warning: detected `float(` in Python edit (action already occurred; requires follow-up fix)."
        return "PostToolUse lint check: clean."
    return "PostToolUse: no check configured for this tool."


def run_tool_pipeline(description: str, tool_name: str, target_arg: str, payload: str = "") -> None:
    """Run a candidate tool call through PreToolUse, Execution, and PostToolUse."""
    print(f"--- Scenario: {description} ---")
    print(f"  Proposed Tool Call : {tool_name}({target_arg})")
    allowed, pre_msg = evaluate_pre_tool_use(tool_name, target_arg)
    print(f"  1. Pre-Action Gate : {pre_msg}")
    if not allowed:
        print("  2. Tool Execution  : SKIPPED (prevented before side effect)")
        print("  3. Post-Action Hook: N/A\n")
        return

    print("  2. Tool Execution  : EXECUTED on workspace")
    post_msg = evaluate_post_tool_use(tool_name, target_arg, payload)
    print(f"  3. Post-Action Hook: {post_msg}\n")


def main() -> None:
    print("Advisory Guidance loaded in CLAUDE.md (guides model reasoning, not an access control):")
    for rule in ADVISORY_CLAUDE_MD_RULES:
        print(f"  * {rule}")
    print("")

    run_tool_pipeline(
        "Attempt to edit a locked migration file",
        tool_name="Edit",
        target_arg="migrations/locked/0001_init.sql",
        payload="ALTER TABLE orders DROP COLUMN audit_id;",
    )

    run_tool_pipeline(
        "Edit pricing module with a float conversion",
        tool_name="Edit",
        target_arg="services/orders/pricing.py",
        payload="discount = float(amount) * 0.10",
    )

    run_tool_pipeline(
        "Edit pricing module with integer cents",
        tool_name="Edit",
        target_arg="services/orders/pricing.py",
        payload="discount_cents = (amount_cents * basis_points) // 10_000",
    )

    print(
        "Takeaway: Use CLAUDE.md and `.claude/rules/` to guide coding conventions, permissions and "
        "blocking PreToolUse hooks to stop disallowed tool actions before they run, and PostToolUse "
        "hooks for post-edit linting—backed by OS/credential permissions and CI."
    )


if __name__ == "__main__":
    main()

