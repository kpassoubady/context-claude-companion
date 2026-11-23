# Lab 1.1: Noisy vs. Focused Context Payloads (Solution)

Finished, runnable reference for the Lab 1.1 notebook. Run it to see the result without doing the exercise. To do the exercise yourself, start in [`../start/`](../start/README.md).

**Goal:** Measure how a noisy context dump dilutes project rules, flag untrusted issue text, and verify two candidate patches against project invariants.

**Needs:** Python 3.10+ standard library only. No API key. No fixtures.

## Run it

**Option 1: print the results in your terminal** (needs Jupyter, for example `pip install notebook`). From this folder:

```bash
jupyter nbconvert --to markdown --execute --stdout lab1_1_noisy_vs_focused_context.ipynb
```

This runs every cell and prints each cell's code with its output. To see only the verdicts, filter for the check lines:

```bash
jupyter nbconvert --to markdown --execute --stdout lab1_1_noisy_vs_focused_context.ipynb 2>/dev/null | grep -E "^ +(PASS|TODO)  "
```

**Option 2: open it.** Run `jupyter notebook lab1_1_noisy_vs_focused_context.ipynb` and choose **Run > Run All Cells**, or use Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab1_1_noisy_vs_focused_context/solution/lab1_1_noisy_vs_focused_context.ipynb)

**Success looks like:** every `check(...)` line prints `PASS` and the last cell prints `Lab complete.`

## What you should see

```text
Snapshot                     | Est. Tokens |  Signal % | Tokens After Rules
----------------------------------------------------------------------------
Noisy Context Dump           |       7,504 |      2.5% |              7,407
Engineered Focused Context   |         222 |    100.0% |                125

PASS  Noisy snapshot is about 7,504 estimated tokens
PASS  Noisy snapshot is only 2.5% high signal
PASS  Noisy constraint distance is 7,407 tokens
PASS  Focused snapshot is 222 tokens, 100% signal, 125 tokens after the rules

Flagged untrusted phrases in issue comment: ['ignore previous rules', 'without idempotency_key', 'use fast float']
PASS  All three injection phrases are flagged in the issue comment
PASS  The trusted CLAUDE.md text is not flagged

Drifted float patch (followed noisy issue hint): {'decimal_invariant': False, 'idempotency_invariant': False, 'acceptance_test': False}
Focused Decimal patch (followed CLAUDE.md rules): {'decimal_invariant': True, 'idempotency_invariant': True, 'acceptance_test': True}
PASS  Drifted float patch fails every gate
PASS  Focused Decimal patch passes every gate

Lab complete.
```

## How to read the result

- **Noisy vs. focused:** the noisy dump is 7,504 estimated tokens and only 2.5% high signal, with 7,407 tokens sitting *after* `CLAUDE.md`. The focused snapshot is 222 tokens, 100% signal, 125 tokens after the rules. Same task, about 34x fewer tokens, and the rules stay close to the end of the window.
- **Untrusted text:** the issue comment trips all three injection phrases; the trusted `CLAUDE.md` trips none.
- **Patch verification:** the patch that followed the issue comment (floats, no idempotency check) fails all three gates. The patch that followed `CLAUDE.md` (Decimal, idempotency key, half-even rounding of 10.125 to 10.12) passes all three.

## Takeaway

Context engineering curates high-signal instructions, targeted file slices, and bounded test outputs, and treats retrieved comments and logs as untrusted evidence.
