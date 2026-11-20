#!/usr/bin/env python3
"""PreToolUse hook: block edits to locked migrations and recursive deletes.

Claude Code passes the pending tool call as JSON on stdin. Exit code 2 blocks
the call and feeds stderr back to Claude. Exit code 0 lets the call proceed.
"""
import fnmatch
import json
import os
import sys

event = json.load(sys.stdin)
tool_input = event.get("tool_input", {})
file_path = os.path.relpath(os.path.realpath(tool_input["file_path"]), os.path.realpath(".")) if tool_input.get("file_path") else ""
command = tool_input.get("command", "")

if file_path and fnmatch.fnmatch(file_path, "migrations/locked/*"):
    print(f"Blocked: {file_path} is a locked migration.", file=sys.stderr)
    sys.exit(2)
if command.startswith("rm -rf"):
    print("Blocked: recursive delete is not allowed.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
