# Lab 4.2: Context A/B/C Scorecard Evaluator (Solution)

Finished, runnable reference for the Lab 4.2 notebook. Run it to see the result without doing the exercise. To do the exercise yourself, start in [`../start/`](../start/README.md).

**Goal:** Evaluate three context configurations against the same coding task using mandatory correctness, instruction adherence, and safety gates before comparing token and turn efficiency.

**Needs:** Python 3.10+ standard library only. No API key. No fixtures.

## Run it

**Option 1: print the results in your terminal** (needs Jupyter, for example `pip install notebook`). From this folder:

```bash
jupyter nbconvert --to markdown --execute --stdout lab4_2_context_ab_evaluator.ipynb
```

This runs every cell and prints each cell's code with its output. To see only the verdicts, filter for the check lines:

```bash
jupyter nbconvert --to markdown --execute --stdout lab4_2_context_ab_evaluator.ipynb 2>/dev/null | grep -E "^ +(PASS|TODO)  "
```

**Option 2: open it.** Run `jupyter notebook lab4_2_context_ab_evaluator.ipynb` and choose **Run > Run All Cells**, or use Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab4_2_context_ab_evaluator/solution/lab4_2_context_ab_evaluator.ipynb)

**Success looks like:** every `check(...)` line prints `PASS` and the last cell prints `Lab complete.`

## What you should see

```text
=== Controlled Context Evaluation Scorecard (Evidence Type: synthetic) ===
Variant                                  | Tests | Rules | Safety |  /context | Turns | /cost | Verdict
--------------------------------------------------------------------------------------------------------------------------
Variant A (Bloated & Conflicting)        | 4/5   | 2/3   | PASS   |    24,800 |     6 |   N/A | REJECTED (failed acceptance tests)
Variant B (Over-Trimmed 'Token Miser')   | 3/5   | 1/3   | FAIL   |     6,200 |     2 |   N/A | REJECTED (failed acceptance tests)
Variant C (Engineered Scoped Context)    | 5/5   | 3/3   | PASS   |    11,400 |     3 |   N/A | ELIGIBLE (passes all primary gates; compare efficiency)

Selected Configuration: Variant C (Engineered Scoped Context)
Notice: Variant B used the fewest tokens (6,200) and turns (2) but was automatically rejected because it failed acceptance tests and safety gates.

PASS  Variants A and B are rejected, C is eligible
PASS  Variant B has the lowest token count of all three
PASS  Variant C is selected even though B used fewer tokens

Lab complete.
```

## How to read the result

- **Variant B is the cheapest** (6,200 tokens, 2 turns) **and is rejected:** 3 of 5 tests pass and the safety gate fails. Saving tokens does not buy back a failed gate.
- **Variant A passes safety but fails tests** (4 of 5) and is the most expensive (24,800 tokens).
- **Variant C is the only eligible variant** (5/5 tests, 3/3 rules, safety pass) and is selected at 11,400 tokens. Efficiency is compared only among variants that pass every gate.

## Takeaway

Gate context changes on task correctness, instruction adherence, and safety first. Compare `/context`, `/cost`, and turn counts only among passing configurations.
