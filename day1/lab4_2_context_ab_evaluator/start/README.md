# Lab 4.2: Context A/B/C Scorecard Evaluator (Start)

> **Short on time, or want to see the finished result first?** Run the reference notebook in [`../solution/`](../solution/README.md) instead. It needs no editing.

**Day 1, Topic 4.** Notebook version of the instructor demo [`demo-context-ab-evaluator.py`](../../demos/demo-context-ab-evaluator.py).

**Goal:** Evaluate three context configurations against the same coding task using mandatory correctness, instruction adherence, and safety gates before comparing token and turn efficiency.

## What you will be able to do

1. Apply quality-first gates (tests, instruction adherence, safety) to a context configuration.
2. Select the cheapest configuration only among those that pass every gate.
3. Explain why fewer tokens or turns never excuse a failed quality or safety gate.

## Before you start

- Python 3.10+ standard library only. No API key. No fixtures.
- Local Jupyter: activate your Python environment first (`source venv/bin/activate` on macOS and Linux, `venv\Scripts\activate` on Windows). See the [setup guide](../../../README.md) for installation.
- Google Colab needs nothing installed.

## Open the notebook

- **Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab4_2_context_ab_evaluator/start/lab4_2_context_ab_evaluator.ipynb)
- **Local Jupyter:** from this folder run `jupyter notebook lab4_2_context_ab_evaluator.ipynb`

## How the notebook is organized

Work top to bottom and run every cell in order. Every `# TODO` comment marks code you write. Below each TODO block, `check(...)` lines print `PASS` when your result is correct and `TODO` while a step is unfinished. Compare your output with the `# Expected:` comment in the cell.

## Step 0 - Run the setup cells

Run the `check()` cell and Section 1. It defines three labeled, synthetic benchmark records for the same coding task: a bloated and conflicting baseline (A), an over-trimmed "token miser" (B), and an engineered scoped context (C). The numbers are synthetic; with a real comparison you would replace them with your own `/context` and `/cost` readings.

## Step 1 - Apply the decision rule (Section 2)

Implement the three gates in `evaluate_variant(v)`. Replace the `tests_ok = adherence_ok = safety_ok = False` placeholder line:

- [ ] `tests_ok` is true when `v["tests_passed"] == v["tests_total"]`.
- [ ] `adherence_ok` is true when every value in `v["invariants"]` is true (hint: `all(...)`).
- [ ] `safety_ok` is `bool(v["safety_gate_passed"])`.

**Expected output:** No output of its own. Step 3 prints the scorecard.

## Step 2 - Select the winner (Section 3)

Implement `select_winner(evaluated)`:

- [ ] Keep only the rows where `row["eligible"]` is true.
- [ ] Return the eligible row with the smallest `context_tokens` (hint: `min(..., key=lambda r: r["context_tokens"])`).
- [ ] Return `None` when no variant is eligible.

**Expected output:** No output of its own. Step 3 prints the scorecard.

## Step 3 - Run the scorecard (Section 4)

No new code. Run the scorecard cell. With the placeholders in place every variant shows `REJECTED` and no winner is selected; once both functions are done:

**Expected output:**

```text
Variant A (Bloated & Conflicting)        | 4/5   | 2/3   | PASS   |    24,800 |     6 |   N/A | REJECTED (failed acceptance tests)
Variant B (Over-Trimmed 'Token Miser')   | 3/5   | 1/3   | FAIL   |     6,200 |     2 |   N/A | REJECTED (failed acceptance tests)
Variant C (Engineered Scoped Context)    | 5/5   | 3/3   | PASS   |    11,400 |     3 |   N/A | ELIGIBLE (passes all primary gates; compare efficiency)

Selected Configuration: Variant C (Engineered Scoped Context)
```

**These checks should print `PASS`:**

- Variants A and B are rejected, C is eligible
- Variant B has the lowest token count of all three
- Variant C is selected even though B used fewer tokens

## Done when

Every `check(...)` line prints `PASS`, and the last cell prints `Lab complete.` and a one-line takeaway.

## Getting stuck?

Try each TODO on your own first. Then compare with the finished notebook in [`../solution/`](../solution/README.md), which also lists the complete expected output.
