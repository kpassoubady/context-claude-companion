# Lab 3.3: Subagent Isolation vs. Inline Search

Notebook version of the instructor demo `../demos/demo-subagent-isolation-vs-inline-search.py`. No API key needed. Needs python3, git, and grep (all present in Colab).

## Objectives

By the end of this lab you will be able to:

1. Measure the tokens a targeted grep adds to the parent window.
2. Model what a subagent returns to the parent versus what its own window absorbs.
3. Decide when local `grep` and `git` are enough and when an external index is justified.

## Setup

Activate your Python environment before running any cells (skip this in Colab):

```bash
# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

See the [setup guide](../../README.md) for full installation instructions.

## Instructions

1. Open `start/lab3_3_subagent_isolation_vs_inline_search.ipynb` in Google Colab or locally in Jupyter.
2. Read each markdown cell for context.
3. Find the `# TODO` comments and implement the required code.
4. Run each cell in order. The `check(...)` lines print `PASS` when your result is correct and `TODO` while a step is unfinished. Compare your output with the expected result shown in the comments.

**Run command (local Jupyter):**

```bash
jupyter notebook start/lab3_3_subagent_isolation_vs_inline_search.ipynb
```

**Open in Colab:**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab3_3_subagent_isolation_vs_inline_search/start/lab3_3_subagent_isolation_vs_inline_search.ipynb)

## Getting Stuck?

The `solution/` directory contains a fully working reference notebook. Try each TODO on your own first, then compare with the solution.
