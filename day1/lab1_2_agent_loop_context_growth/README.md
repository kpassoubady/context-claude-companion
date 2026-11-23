# Lab 1.2: Multi-Turn Agent Loop Context Growth

Notebook version of the instructor demo `../demos/demo-agent-loop-context-growth.py`. No API key needed. Needs python3, pytest, git, and grep (all present in Colab).

## Objectives

By the end of this lab you will be able to:

1. Measure the real lines and estimated tokens each tool call adds to the window.
2. Scope `ls`, `grep`, `cat`, `pytest`, and `git diff` commands so build output and vendored code stay out of context.
3. Explain why every turn's output stays in the window for all later turns.

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

1. Open `start/lab1_2_agent_loop_context_growth.ipynb` in Google Colab or locally in Jupyter.
2. Read each markdown cell for context.
3. Find the `# TODO` comments and implement the required code.
4. Run each cell in order. The `check(...)` lines print `PASS` when your result is correct and `TODO` while a step is unfinished. Compare your output with the expected result shown in the comments.

**Run command (local Jupyter):**

```bash
jupyter notebook start/lab1_2_agent_loop_context_growth.ipynb
```

**Open in Colab:**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab1_2_agent_loop_context_growth/start/lab1_2_agent_loop_context_growth.ipynb)

## Getting Stuck?

The `solution/` directory contains a fully working reference notebook. Try each TODO on your own first, then compare with the solution.
