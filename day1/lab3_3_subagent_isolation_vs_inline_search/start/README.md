# Lab 3.3: Subagent Isolation vs. Inline Search (Start)

> **Short on time, or want to see the finished result first?** Run the reference notebook in [`../solution/`](../solution/README.md) instead. It needs no editing.

**Day 1, Topic 3.** Notebook version of the instructor demo [`demo-subagent-isolation-vs-inline-search.py`](../../demos/demo-subagent-isolation-vs-inline-search.py).

**Goal:** Measure what lands in the parent context window for a targeted inline search, a broad inline exploration, and the same exploration delegated to a subagent, then check when local `grep` beats an external index.

## What you will be able to do

1. Measure the tokens a targeted `grep` adds to the parent window.
2. Model what a subagent returns to the parent versus what its own window absorbs.
3. Decide when local `grep` and `git` are enough and when an external index is justified.

## Before you start

- Python 3.10+, `git`, and `grep` (all present in Colab). No API key. No fixtures: the notebook builds its own service tree.
- Local Jupyter: activate your Python environment first (`source venv/bin/activate` on macOS and Linux, `venv\Scripts\activate` on Windows). See the [setup guide](../../../README.md) for installation.
- Google Colab needs nothing installed.

## Open the notebook

- **Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab3_3_subagent_isolation_vs_inline_search/start/lab3_3_subagent_isolation_vs_inline_search.ipynb)
- **Local Jupyter:** from this folder run `jupyter notebook lab3_3_subagent_isolation_vs_inline_search.ipynb`

## How the notebook is organized

Work top to bottom and run every cell in order. Every `# TODO` comment marks code you write. Below each TODO block, `check(...)` lines print `PASS` when your result is correct and `TODO` while a step is unfinished. Compare your output with the `# Expected:` comment in the cell.

## Step 0 - Run the setup cells

Run the imports cell and Section 1. The helper builds a 12-module service tree and a git repo in a temporary folder: two modules define `verify_idempotency_token`, three call it, and seven only mention idempotency in a docstring. That is the noise a broad search has to read past. The broad-search helper in Section 3 is provided.

## Step 1 - Targeted inline search (Section 2)

Implement `targeted_inline(root)`, which returns `(tokens, defs, callers)`:

- [ ] `hits = sh(root, f"grep -rn {SYMBOL} services")`. Every line looks like `path:line:text`.
- [ ] `defs`: the sorted set of file paths (text before the first `:`) for hit lines containing `f"def {SYMBOL}"`.
- [ ] `tokens`: `est_tokens(hits)` plus `est_tokens(sh(root, f"cat {path}"))` for each path in `defs`.
- [ ] `callers`: the sorted set of file paths for hit lines that do **not** contain `f"def {SYMBOL}"`.

**Expected output:**

```text
Targeted inline search: 823 tokens
  defined in: ['services/mod_04/handler.py', 'services/mod_09/handler.py']
  called from: ['services/mod_02/handler.py', 'services/mod_07/handler.py', 'services/mod_11/handler.py']
```

**These checks should print `PASS`:**

- Targeted inline search costs 823 tokens
- Two defining modules found
- Three calling modules found

## Step 2 - Model the subagent (Section 3)

Implement `subagent_footprint(broad_tokens, report)`, which returns `(parent, subagent, total)`. No Claude Code subagent is launched; the child window receives the same real tool output and the parent receives only a short report:

- [ ] The subagent reads everything the broad inline search reads, so its window is `broad_tokens`.
- [ ] The parent window receives only the short report, so its size is `est_tokens(report)`.
- [ ] Total model work is the parent window plus the subagent window.

**Expected output:**

```text
Mode                                               | Parent window | Subagent window | Total model work
--------------------------------------------------------------------------------------------------------
A. Inline, targeted (grep symbol + read 2 files)   |           823 |               0 |              823
B. Inline, broad (read every module that matches)  |         4,404 |               0 |            4,404
C. Subagent, same broad exploration (modeled)      |            67 |           4,404 |            4,471
```

**These checks should print `PASS`:**

- Broad inline exploration costs 4,404 tokens
- The subagent's parent window is only 67 tokens
- The subagent still does 4,471 tokens of total model work
- Delegation keeps the parent smaller than even the targeted inline search

## Step 3 - Local grep vs. an external index (Section 4)

No new code. Run the cell: three tasks, three answers, each backed by a real command on the repo.

**Expected output:**

```text
Task: callers of `verify_idempotency_token` in this repo
  grep hits: 5 -> local Grep + Read
Task: find an uncommitted edit made after the index was built
  index snapshot hits: 0; grep hits: 1; git diff:  1 file changed, 3 insertions(+)
Task: search 4,000 historical postmortems across 15 teams
  grep hits in this repo: 0 -> corpus is not local; use an access-controlled retrieval service (not run here)
```

**These checks should print `PASS`:**

- Scenario 1: grep finds all 5 references to the symbol
- Scenario 2: the stale index misses the new edit, grep and git diff see it
- Scenario 3: the postmortem corpus is not on disk

## Done when

Every `check(...)` line prints `PASS`, and the last cell prints `Lab complete.` and a one-line takeaway.

## Getting stuck?

Try each TODO on your own first. Then compare with the finished notebook in [`../solution/`](../solution/README.md), which also lists the complete expected output.
