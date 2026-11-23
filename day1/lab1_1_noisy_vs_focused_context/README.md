# Lab 1.1: Noisy vs. Focused Context Payloads

Notebook version of the instructor demo `../demos/demo-noisy-vs-focused-context.py`. No API key needed. Pure Python standard library.

## Objectives

By the end of this lab you will be able to:

1. Calculate the signal percentage and constraint distance of a context snapshot.
2. Flag prompt-injection phrases in retrieved issue comments and logs.
3. Verify candidate code against project invariants with AST inspection and a deterministic test.

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

1. Open `start/lab1_1_noisy_vs_focused_context.ipynb` in Google Colab or locally in Jupyter.
2. Read each markdown cell for context.
3. Find the `# TODO` comments and implement the required code.
4. Run each cell in order. The `check(...)` lines print `PASS` when your result is correct and `TODO` while a step is unfinished. Compare your output with the expected result shown in the comments.

**Run command (local Jupyter):**

```bash
jupyter notebook start/lab1_1_noisy_vs_focused_context.ipynb
```

**Open in Colab:**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab1_1_noisy_vs_focused_context/start/lab1_1_noisy_vs_focused_context.ipynb)

## Getting Stuck?

The `solution/` directory contains a fully working reference notebook. Try each TODO on your own first, then compare with the solution.
