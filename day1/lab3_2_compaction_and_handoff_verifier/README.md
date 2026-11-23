# Lab 3.2: Compaction and Handoff Verifier

Notebook version of the instructor demo `../demos/demo-compaction-and-handoff-verifier.py`. No API key needed. Needs python3, pytest, and git; the lab reads fixtures from the companion repo.

## Objectives

By the end of this lab you will be able to:

1. Collect ground truth from `git status`, `pytest`, and `ast` instead of trusting a summary.
2. Audit a summary for the failing test, the rejected approaches, and the method signature.
3. Spot a summary that points the next step at a file git shows untouched.

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

1. Open `start/lab3_2_compaction_and_handoff_verifier.ipynb` in Google Colab or locally in Jupyter.
2. Read each markdown cell for context.
3. Find the `# TODO` comments and implement the required code.
4. Run each cell in order. The `check(...)` lines print `PASS` when your result is correct and `TODO` while a step is unfinished. Compare your output with the expected result shown in the comments.

**Run command (local Jupyter):**

```bash
jupyter notebook start/lab3_2_compaction_and_handoff_verifier.ipynb
```

**Open in Colab:**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab3_2_compaction_and_handoff_verifier/start/lab3_2_compaction_and_handoff_verifier.ipynb)

## Getting Stuck?

The `solution/` directory contains a fully working reference notebook. Try each TODO on your own first, then compare with the solution.
