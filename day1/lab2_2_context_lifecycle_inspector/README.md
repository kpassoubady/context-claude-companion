# Lab 2.2: Context Lifecycle Inspector

Notebook version of the instructor demo `../demos/demo-context-lifecycle-inspector.py`. No API key needed. Python 3 standard library only; the lab reads fixtures from the companion repo.

## Objectives

By the end of this lab you will be able to:

1. Parse `paths:` frontmatter from a `.claude/rules/` file.
2. Decide which rules load at startup and which load only when a matching file is accessed.
3. Compare the active guidance against one monolithic `CLAUDE.md`.

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

1. Open `start/lab2_2_context_lifecycle_inspector.ipynb` in Google Colab or locally in Jupyter.
2. Read each markdown cell for context.
3. Find the `# TODO` comments and implement the required code.
4. Run each cell in order. The `check(...)` lines print `PASS` when your result is correct and `TODO` while a step is unfinished. Compare your output with the expected result shown in the comments.

**Run command (local Jupyter):**

```bash
jupyter notebook start/lab2_2_context_lifecycle_inspector.ipynb
```

**Open in Colab:**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab2_2_context_lifecycle_inspector/start/lab2_2_context_lifecycle_inspector.ipynb)

## Getting Stuck?

The `solution/` directory contains a fully working reference notebook. Try each TODO on your own first, then compare with the solution.
