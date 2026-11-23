# Lab 2.3: Instructions vs. Permissions and Hooks (Solution)

Finished, runnable reference for the Lab 2.3 notebook. Run it to see the result without doing the exercise. To do the exercise yourself, start in [`../start/`](../start/README.md).

**Goal:** Show that `CLAUDE.md` is advice, while a `PreToolUse` hook can block a tool call before it runs and a `PostToolUse` hook can only report after the write.

**Needs:** Python 3.10+ standard library only. No API key. Runs the real hook scripts in `day1/demos/fixtures/hooks_repo/` on a temporary copy: run from inside your clone, or in Colab where the first cells clone the repo.

## Run it

**Option 1: print the results in your terminal** (needs Jupyter, for example `pip install notebook`). From this folder:

```bash
jupyter nbconvert --to markdown --execute --stdout lab2_3_instructions_vs_permissions_hooks.ipynb
```

This runs every cell and prints each cell's code with its output. To see only the verdicts, filter for the check lines:

```bash
jupyter nbconvert --to markdown --execute --stdout lab2_3_instructions_vs_permissions_hooks.ipynb 2>/dev/null | grep -E "^ +(PASS|TODO)  "
```

**Option 2: open it.** Run `jupyter notebook lab2_3_instructions_vs_permissions_hooks.ipynb` and choose **Run > Run All Cells**, or use Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab2_3_instructions_vs_permissions_hooks/solution/lab2_3_instructions_vs_permissions_hooks.ipynb)

**Success looks like:** every `check(...)` line prints `PASS` and the last cell prints `Lab complete.`

## What you should see

```text
CLAUDE.md (advice the model may or may not follow):
  - Use integer cents for monetary fields in `services/orders/`.
  - Do not edit locked migration files under `migrations/locked/`.

permissions.deny in settings.json (enforced by Claude Code, listed here, not evaluated):
  Edit(migrations/locked/**)
  Write(migrations/locked/**)
  Bash(rm -rf *)

Hooks registered in settings.json:
  PreToolUse   matcher=Edit|Write|Bash -> python3 .claude/hooks/pre_tool_use.py
  PostToolUse  matcher=Edit|Write     -> python3 .claude/hooks/post_tool_use.py

['python3 .claude/hooks/pre_tool_use.py']
[]
PASS  Edit triggers the PreToolUse hook
PASS  Bash triggers no PostToolUse hook

--- 1. Edit a locked migration ---
  Tool call      : Edit migrations/locked/0001_init.sql
  PreToolUse     : `python3 .claude/hooks/pre_tool_use.py` -> exit 2, stderr: Blocked: migrations/locked/0001_init.sql is a locked migration.
  Tool executed  : NO (blocked before any side effect)
  File on disk   : e0681a7a -> e0681a7a (unchanged)

--- 2. Edit pricing with a float conversion ---
  Tool call      : Edit services/orders/pricing.py
  PreToolUse     : `python3 .claude/hooks/pre_tool_use.py` -> exit 0
  Tool executed  : YES
  PostToolUse    : `python3 .claude/hooks/post_tool_use.py` -> exit 2, stderr: services/orders/pricing.py: float() on line 2; use integer cents.
  File on disk   : 4b23b7aa -> 2bd688b8 (CHANGED, write already happened)

--- 3. Edit pricing with integer cents ---
  Tool call      : Edit services/orders/pricing.py
  PreToolUse     : `python3 .claude/hooks/pre_tool_use.py` -> exit 0
  Tool executed  : YES
  PostToolUse    : `python3 .claude/hooks/post_tool_use.py` -> exit 0
  File on disk   : 2bd688b8 -> 2daf1456 (CHANGED, write already happened)

--- 4. Recursive delete ---
  Tool call      : Bash rm -rf migrations
  PreToolUse     : `python3 .claude/hooks/pre_tool_use.py` -> exit 2, stderr: Blocked: recursive delete is not allowed.
  Tool executed  : NO (blocked before any side effect)

PASS  Scenario 1: PreToolUse blocks the locked migration and the file is unchanged
PASS  Scenario 2: the float edit is allowed and the write already happened
PASS  Scenario 3: the integer-cents edit is allowed
PASS  Scenario 4: the recursive delete is blocked

Lab complete.
```

The file hashes (`e0681a7a`, ...) come from the fixture content, so they should match yours.

## How to read the result

- **Scenarios 1 and 4:** the `PreToolUse` hook exits 2, so Claude Code never runs the tool. The locked migration's hash does not change.
- **Scenario 2 is the one to study:** the float edit passes `PreToolUse`, the write happens, and only then does `PostToolUse` exit 2 with a complaint. The hash changed. A `PostToolUse` hook can report; it cannot undo.
- **Scenario 3:** an integer-cents edit passes both hooks.
- **Layers:** `CLAUDE.md` is advice, `permissions.deny` and `PreToolUse` hooks enforce before the call, and `PostToolUse` only observes.

## Takeaway

`CLAUDE.md` steers, a `PreToolUse` hook stops the call before it runs (exit 2), and a `PostToolUse` hook only reports after the write. Back both with OS permissions and CI.
