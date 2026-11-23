# Lab 2.3: Instructions vs. Permissions and Hooks (Start)

> **Short on time, or want to see the finished result first?** Run the reference notebook in [`../solution/`](../solution/README.md) instead. It needs no editing.

**Day 1, Topic 2.** Notebook version of the instructor demo [`demo-instructions-vs-permissions-hooks.py`](../../demos/demo-instructions-vs-permissions-hooks.py).

**Goal:** Show that `CLAUDE.md` is advice, while a `PreToolUse` hook can block a tool call before it runs and a `PostToolUse` hook can only report after the write.

## What you will be able to do

1. Select the hooks registered for a tool call by matcher regex.
2. Run a hook script with the Claude Code hook protocol: JSON on stdin, and exit code 2 blocks the call.
3. Explain why a `PostToolUse` hook cannot undo a write that already happened.

## Before you start

- Python 3.10+ standard library only. No API key. Runs the real hook scripts in `day1/demos/fixtures/hooks_repo/` on a temporary copy: run from inside your clone, or in Colab where the first cells clone the repo.
- Local Jupyter: activate your Python environment first (`source venv/bin/activate` on macOS and Linux, `venv\Scripts\activate` on Windows). See the [setup guide](../../../README.md) for installation.
- Google Colab needs nothing installed.

## Open the notebook

- **Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab2_3_instructions_vs_permissions_hooks/start/lab2_3_instructions_vs_permissions_hooks.ipynb)
- **Local Jupyter:** from this folder run `jupyter notebook lab2_3_instructions_vs_permissions_hooks.ipynb`

## How the notebook is organized

Work top to bottom and run every cell in order. Every `# TODO` comment marks code you write. Below each TODO block, `check(...)` lines print `PASS` when your result is correct and `TODO` while a step is unfinished. Compare your output with the `# Expected:` comment in the cell.

## Step 0 - Run the setup cells

Run the imports cell and Section 1. It lists the three layers of control in the fixture repo: advisory prose in `CLAUDE.md`, `permissions.deny` rules (listed, not evaluated), and two hook scripts registered in `settings.json`. `run_scenario()` in Section 4 is provided.

## Step 1 - Find the hooks for a tool call (Section 2)

Implement `hooks_for(settings, event, tool_name)`:

- [ ] Loop over the entries in `settings.get("hooks", {}).get(event, [])`.
- [ ] Keep an entry only when `re.fullmatch(entry.get("matcher", ".*"), tool_name)` is truthy.
- [ ] For a kept entry, add `h["command"]` to `commands` for every hook `h` in `entry["hooks"]` whose `h["type"] == "command"`.

**Expected output:**

```text
['python3 .claude/hooks/pre_tool_use.py']
[]
```

**These checks should print `PASS`:**

- Edit triggers the PreToolUse hook
- Bash triggers no PostToolUse hook

## Step 2 - Run a hook script (Section 3)

Implement `run_hook(command, root, event, tool_name, tool_input)` the way Claude Code runs a hook:

- [ ] Run `command` with `subprocess.run(command, shell=True, cwd=root, capture_output=True, text=True, input=...)`.
- [ ] Pass `json.dumps(payload)` as `input=`: the hook protocol sends the tool call as JSON on stdin.
- [ ] Return `(proc.returncode, proc.stderr.strip())`. Exit code 2 means "block the tool call", and stderr goes back to Claude.

**Expected output:** No output of its own. Step 3 exercises it.

## Step 3 - Run four scenarios (Section 4)

No new code. Run the scenarios cell and read each block: was the tool executed, what did each hook return, did the file hash change?

**Expected output:**

```text
1. Edit a locked migration:          PreToolUse exit 2, tool NOT executed, file unchanged
2. Edit pricing with float():       PreToolUse exit 0, tool executed, PostToolUse exit 2, file CHANGED
3. Edit pricing with integer cents: both hooks exit 0, file changed
4. Recursive delete (rm -rf):       PreToolUse exit 2, tool NOT executed
```

This is a condensed view. Your terminal prints a longer block per scenario (tool call, hook command, exit code, stderr, file hash before and after); the full text is in `../solution/README.md`.

**These checks should print `PASS`:**

- Scenario 1: PreToolUse blocks the locked migration and the file is unchanged
- Scenario 2: the float edit is allowed and the write already happened
- Scenario 3: the integer-cents edit is allowed
- Scenario 4: the recursive delete is blocked

## Done when

Every `check(...)` line prints `PASS`, and the last cell prints `Lab complete.` and a one-line takeaway.

## Getting stuck?

Try each TODO on your own first. Then compare with the finished notebook in [`../solution/`](../solution/README.md), which also lists the complete expected output.
