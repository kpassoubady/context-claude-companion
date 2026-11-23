# Lab 1.1: Noisy vs. Focused Context Payloads (Start)

> **Short on time, or want to see the finished result first?** Run the reference notebook in [`../solution/`](../solution/README.md) instead. It needs no editing.

**Day 1, Topic 1.** Notebook version of the instructor demo [`demo-noisy-vs-focused-context.py`](../../demos/demo-noisy-vs-focused-context.py).

**Goal:** Measure how a noisy context dump dilutes project rules, flag untrusted issue text, and verify two candidate patches against project invariants.

## What you will be able to do

1. Calculate the signal percentage and constraint distance of a context snapshot.
2. Flag prompt-injection phrases in retrieved issue comments and logs.
3. Verify candidate code against project invariants with AST inspection and a deterministic test.

## Before you start

- Python 3.10+ standard library only. No API key. No fixtures.
- Local Jupyter: activate your Python environment first (`source venv/bin/activate` on macOS and Linux, `venv\Scripts\activate` on Windows). See the [setup guide](../../../README.md) for installation.
- Google Colab needs nothing installed.

## Open the notebook

- **Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab1_1_noisy_vs_focused_context/start/lab1_1_noisy_vs_focused_context.ipynb)
- **Local Jupyter:** from this folder run `jupyter notebook lab1_1_noisy_vs_focused_context.ipynb`

## How the notebook is organized

Work top to bottom and run every cell in order. Every `# TODO` comment marks code you write. Below each TODO block, `check(...)` lines print `PASS` when your result is correct and `TODO` while a step is unfinished. Compare your output with the `# Expected:` comment in the cell.

## Step 0 - Run the setup cells

Cells 1-2 hold the imports and the `check()` helper. Section 1 defines the context segments (rules, an untrusted issue comment, a noisy test log, one focused failure, the source to edit). Run them as they are; read the issue comment, because it tries to override the project rules.

## Step 1 - Measure a context snapshot (Section 2)

Implement `analyze_context_snapshot(name, segments)`:

- [ ] Loop over `segments`, unpacking `(seg_name, content, is_high_signal)`, and compute `seg_tokens = estimate_tokens(content)`.
- [ ] Add `seg_tokens` to `total_tokens`, and also to `signal_tokens` when `is_high_signal` is true.
- [ ] When `seg_name == "CLAUDE.md"` set `seen_rules = True`; for every *later* segment add `seg_tokens` to `tokens_after_rules`. Use `if` / `elif` so the `CLAUDE.md` segment itself is not counted as "after the rules".

**Expected output:**

```text
Snapshot                     | Est. Tokens |  Signal % | Tokens After Rules
----------------------------------------------------------------------------
Noisy Context Dump           |       7,504 |      2.5% |              7,407
Engineered Focused Context   |         222 |    100.0% |                125
```

**These checks should print `PASS`:**

- Noisy snapshot is about 7,504 estimated tokens
- Noisy snapshot is only 2.5% high signal
- Noisy constraint distance is 7,407 tokens
- Focused snapshot is 222 tokens, 100% signal, 125 tokens after the rules

## Step 2 - Flag untrusted text (Section 3)

Implement `scan_untrusted_input(text)`:

- [ ] Return only the entries of `patterns` that `re.search()` finds in `text`, ignoring case (`flags=re.IGNORECASE`). A list comprehension with an `if` condition does it in one line.

**Expected output:**

```text
Flagged untrusted phrases in issue comment: ['ignore previous rules', 'without idempotency_key', 'use fast float']
```

**These checks should print `PASS`:**

- All three injection phrases are flagged in the issue comment
- The trusted CLAUDE.md text is not flagged

## Step 3 - Verify candidate patches (Section 4)

Implement the AST part of `check_invariants_and_tests(code_str)`:

- [ ] Walk every node with `ast.walk(tree)` and look only at `ast.Name` nodes.
- [ ] Set `uses_decimal = True` when a `Name` node has `id == "Decimal"`.
- [ ] Set `uses_float = True` when a `Name` node has `id == "float"`.

**Expected output:**

```text
Drifted float patch (followed noisy issue hint): {'decimal_invariant': False, 'idempotency_invariant': False, 'acceptance_test': False}
Focused Decimal patch (followed CLAUDE.md rules): {'decimal_invariant': True, 'idempotency_invariant': True, 'acceptance_test': True}
```

**These checks should print `PASS`:**

- Drifted float patch fails every gate
- Focused Decimal patch passes every gate

## Done when

Every `check(...)` line prints `PASS`, and the last cell prints `Lab complete.` and a one-line takeaway.

## Getting stuck?

Try each TODO on your own first. Then compare with the finished notebook in [`../solution/`](../solution/README.md), which also lists the complete expected output.
