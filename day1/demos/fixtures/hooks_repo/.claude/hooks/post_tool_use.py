#!/usr/bin/env python3
"""PostToolUse hook: report float() calls in edited Python files.

Runs after the edit has already been written. Exit code 2 sends stderr back to
Claude so it can fix the file, but it cannot undo the write.
"""
import ast
import json
import os
import sys

event = json.load(sys.stdin)
file_path = event.get("tool_input", {}).get("file_path", "")
if not file_path.endswith(".py"):
    sys.exit(0)

tree = ast.parse(open(file_path).read())
lines = [
    node.lineno
    for node in ast.walk(tree)
    if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "float"
]
if lines:
    rel = os.path.relpath(os.path.realpath(file_path), os.path.realpath("."))
    print(f"{rel}: float() on line {lines[0]}; use integer cents.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
