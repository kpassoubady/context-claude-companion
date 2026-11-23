# Lab 2.3: Instructions vs. Permissions and Hooks

Notebook version of the instructor demo `../demos/demo-instructions-vs-permissions-hooks.py`. No API key needed. Python 3 standard library only; the lab reads fixtures from the companion repo.

## Objectives

By the end of this lab you will be able to:

1. Select the hooks registered for a tool call by matcher regex.
2. Run a hook script with the Claude Code hook protocol: JSON on stdin, and exit code 2 blocks the call.
3. Explain why a `PostToolUse` hook cannot undo a write that already happened.

## Setup

Activate your Python environment before running any cells (skip this in Colab):

```bash
# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

See the [setup guide](../../README.md) for full installation instructions.

In Colab the first cells clone the companion repo so the `day1/demos/fixtures/` files are available. Locally, run the notebook from inside your clone.

## Instructions

1. Open `start/lab2_3_instructions_vs_permissions_hooks.ipynb` in Google Colab or locally in Jupyter.
2. Read each markdown cell for context.
3. Find the `# TODO` comments and implement the required code.
4. Run each cell in order. The `check(...)` lines print `PASS` when your result is correct and `TODO` while a step is unfinished. Compare your output with the expected result shown in the comments.

**Run command (local Jupyter):**

```bash
jupyter notebook start/lab2_3_instructions_vs_permissions_hooks.ipynb
```

**Open in Colab:**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab2_3_instructions_vs_permissions_hooks/start/lab2_3_instructions_vs_permissions_hooks.ipynb)

## Getting Stuck?

The `solution/` directory contains a fully working reference notebook. Try each TODO on your own first, then compare with the solution.
