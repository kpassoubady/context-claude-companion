# Lab 4.2: Context A/B/C Scorecard Evaluator

Notebook version of the instructor demo `../demos/demo-context-ab-evaluator.py`. No API key needed. Pure Python standard library.

## Objectives

By the end of this lab you will be able to:

1. Apply quality-first gates (tests, instruction adherence, safety) to a context configuration.
2. Select the cheapest configuration only among those that pass every gate.
3. Explain why fewer tokens or turns never excuse a failed quality or safety gate.

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

1. Open `start/lab4_2_context_ab_evaluator.ipynb` in Google Colab or locally in Jupyter.
2. Read each markdown cell for context.
3. Find the `# TODO` comments and implement the required code.
4. Run each cell in order. The `check(...)` lines print `PASS` when your result is correct and `TODO` while a step is unfinished. Compare your output with the expected result shown in the comments.

**Run command (local Jupyter):**

```bash
jupyter notebook start/lab4_2_context_ab_evaluator.ipynb
```

**Open in Colab:**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab4_2_context_ab_evaluator/start/lab4_2_context_ab_evaluator.ipynb)

## Getting Stuck?

The `solution/` directory contains a fully working reference notebook. Try each TODO on your own first, then compare with the solution.
