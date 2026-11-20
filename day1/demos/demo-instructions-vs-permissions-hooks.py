"""
Demo - Instructions vs. Permissions and Hooks
Day 1 - Topic 2

Goal: Show that `CLAUDE.md` is advice, while a `PreToolUse` hook can block a tool call before it runs and a `PostToolUse` hook can only report after the write.

This script reads a real `.claude/settings.json` from `fixtures/hooks_repo/`, finds the hooks registered for each tool call by matcher, and runs the real hook scripts as subprocesses using the Claude Code hook protocol (JSON on stdin; exit code 2 blocks and sends stderr back to Claude). It works on a temporary copy of the fixture and prints the hook exit codes, stderr, and whether the file on disk changed. The `permissions.deny` rules in the same file are enforced by Claude Code itself and are only listed here, not evaluated.

No API key needed. Python 3 standard library only.

Run (from the companion repo root): python3 day1/demos/demo-instructions-vs-permissions-hooks.py
"""

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

FIXTURE = Path(__file__).parent / "fixtures" / "hooks_repo"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:8]


def hooks_for(settings: dict, event: str, tool_name: str) -> list[str]:
    """Return hook commands whose matcher regex matches the tool name."""
    commands = []
    for entry in settings.get("hooks", {}).get(event, []):
        if re.fullmatch(entry.get("matcher", ".*"), tool_name):
            commands += [h["command"] for h in entry["hooks"] if h["type"] == "command"]
    return commands


def run_hook(command: str, root: Path, event: str, tool_name: str, tool_input: dict) -> tuple[int, str]:
    payload = {"hook_event_name": event, "tool_name": tool_name, "tool_input": tool_input}
    proc = subprocess.run(
        command, shell=True, cwd=root, input=json.dumps(payload), capture_output=True, text=True
    )
    return proc.returncode, proc.stderr.strip()


def run_scenario(root: Path, settings: dict, title: str, tool_name: str, tool_input: dict, new_content: str = "") -> None:
    target = root / tool_input["file_path"] if "file_path" in tool_input else None
    before = sha(target) if target else "-"
    # Claude Code sends absolute paths; mirror that.
    sent = dict(tool_input, file_path=str(target)) if target else dict(tool_input)

    print(f"--- {title} ---")
    print(f"  Tool call      : {tool_name} {tool_input.get('file_path') or tool_input.get('command')}")

    blocked = False
    for cmd in hooks_for(settings, "PreToolUse", tool_name):
        code, err = run_hook(cmd, root, "PreToolUse", tool_name, sent)
        print(f"  PreToolUse     : `{cmd}` -> exit {code}" + (f", stderr: {err}" if err else ""))
        blocked = blocked or code == 2
    if blocked:
        print("  Tool executed  : NO (blocked before any side effect)")
        if target:
            after = sha(target)
            print(f"  File on disk   : {before} -> {after} ({'unchanged' if before == after else 'CHANGED'})")
        print()
        return

    if target:
        target.write_text(new_content)  # stand-in for the Edit tool performing the write
    print("  Tool executed  : YES")
    for cmd in hooks_for(settings, "PostToolUse", tool_name):
        code, err = run_hook(cmd, root, "PostToolUse", tool_name, sent)
        print(f"  PostToolUse    : `{cmd}` -> exit {code}" + (f", stderr: {err}" if err else ""))
    if target:
        after = sha(target)
        print(f"  File on disk   : {before} -> {after} ({'unchanged' if before == after else 'CHANGED, write already happened'})")
    print()


def main() -> None:
    settings = json.loads((FIXTURE / ".claude" / "settings.json").read_text())

    print("CLAUDE.md (advice the model may or may not follow):")
    for line in (FIXTURE / "CLAUDE.md").read_text().splitlines():
        if line.startswith("- "):
            print(f"  {line}")
    print("\npermissions.deny in settings.json (enforced by Claude Code, listed here, not evaluated):")
    for rule in settings["permissions"]["deny"]:
        print(f"  {rule}")
    print("\nHooks below are the real scripts from fixtures/hooks_repo/.claude/hooks/.\n")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve() / "hooks_repo"
        shutil.copytree(FIXTURE, root)

        run_scenario(
            root, settings, "1. Edit a locked migration", "Edit",
            {"file_path": "migrations/locked/0001_init.sql"},
            "ALTER TABLE orders DROP COLUMN audit_id;",
        )
        run_scenario(
            root, settings, "2. Edit pricing with a float conversion", "Edit",
            {"file_path": "services/orders/pricing.py"},
            "def apply_discount(amount, bps):\n    return float(amount) * 0.10\n",
        )
        run_scenario(
            root, settings, "3. Edit pricing with integer cents", "Edit",
            {"file_path": "services/orders/pricing.py"},
            "def apply_discount(amount_cents, bps):\n    return (amount_cents * bps) // 10_000\n",
        )
        run_scenario(root, settings, "4. Recursive delete", "Bash", {"command": "rm -rf migrations"})

    print(
        "Takeaway: CLAUDE.md steers, a PreToolUse hook stops the call before it runs (exit 2), and a "
        "PostToolUse hook only reports after the write (scenario 2 left the float on disk). Back both "
        "with OS permissions and CI."
    )


if __name__ == "__main__":
    main()
