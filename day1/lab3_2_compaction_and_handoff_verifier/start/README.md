# Lab 3.2: Compaction and Handoff Verifier (Start)

> **Short on time, or want to see the finished result first?** Run the reference notebook in [`../solution/`](../solution/README.md) instead. It needs no editing.

**Day 1, Topic 3.** Notebook version of the instructor demo [`demo-compaction-and-handoff-verifier.py`](../../demos/demo-compaction-and-handoff-verifier.py).

**Goal:** Audit an unfocused auto-compaction summary, a focused `/compact` summary, and a `HANDOFF.md` against what `git status` and `pytest` report for the repository.

## What you will be able to do

1. Collect ground truth from `git status`, `pytest`, and `ast` instead of trusting a summary.
2. Audit a summary for the failing test, the rejected approaches, and the method signature.
3. Spot a summary that points the next step at a file git shows untouched.

## Before you start

- Python 3.10+, `pytest`, and `git`. No API key. Reads `day1/demos/fixtures/compaction_repo/`: run from inside your clone, or in Colab where the first cells clone the repo. The first code cell installs `pytest>=7`.
- Local Jupyter: activate your Python environment first (`source venv/bin/activate` on macOS and Linux, `venv\Scripts\activate` on Windows). See the [setup guide](../../../README.md) for installation.
- Google Colab needs nothing installed.

## Open the notebook

- **Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab3_2_compaction_and_handoff_verifier/start/lab3_2_compaction_and_handoff_verifier.ipynb)
- **Local Jupyter:** from this folder run `jupyter notebook lab3_2_compaction_and_handoff_verifier.ipynb`

## How the notebook is organized

Work top to bottom and run every cell in order. Every `# TODO` comment marks code you write. Below each TODO block, `check(...)` lines print `PASS` when your result is correct and `TODO` while a step is unfinished. Compare your output with the `# Expected:` comment in the cell.

## Step 0 - Run the setup cells

Run the install and imports cells, then Section 1. `compaction_repo` is a refund-ledger bug (separate from Lab 3.1). A helper copies it to a temporary folder, commits a baseline, and applies one in-progress edit to `refunds/ledger.py`, as if you stopped mid-session. `session_history/` holds three summaries of that session; the cell prints the automatic one. The `audit()` helper in Section 3 is provided.

## Step 1 - Collect ground truth (Section 2)

Finish `collect_ground_truth(root)`. Each fact must come from a tool, not from a summary:

- [ ] `modified`: the file path of every `git status --porcelain` line that does **not** start with `??` (the path starts at column 3, so use `line[3:]`).
- [ ] `failing`: `re.findall(r"^FAILED (\S+)", pytest_out, flags=re.M)` returns the failing test ids.
- [ ] `signature`: find the `ast.FunctionDef` named `post_refund` among `ast.walk(tree)` (hint: `next(n for n in ast.walk(tree) if ...)`), then build `f"post_refund({ast.unparse(func.args)}) -> {ast.unparse(func.returns)}"`.

**Expected output:**

```text
=== Ground truth from the repository ===
  git status --porcelain : M refunds/ledger.py
  pytest failing         : tests/test_ledger.py::test_duplicate_delivery_is_not_posted_twice
  signature (ast)        : post_refund(self, order_id: str, amount_cents: int, idempotency_key: str) -> bool
  rejected (transcript)  : ttl_dedupe_cache, global_post_lock
```

**These checks should print `PASS`:**

- Only refunds/ledger.py is modified
- One test fails: test_duplicate_delivery_is_not_posted_twice
- The ast signature of post_refund is extracted

## Step 2 - Compare the three artifacts (Section 4)

No new code. Run the comparison cell. `audit()` checks each summary for four things: does it name the failing test, how many rejected fixes does it keep, does it contain the real signature, and does it name an unmodified file as work in progress.

**Expected output:**

```text
Artifact                       | Failing test | Rejected fixes | Signature | Unmodified files named as work
--------------------------------------------------------------------------------------------------------------
1. Unfocused auto-compaction   | False        | 0/2            | False     | refunds/webhook.py
2. Focused /compact summary    | True         | 2/2            | True      | none
3. HANDOFF.md                  | True         | 2/2            | True      | none
```

**These checks should print `PASS`:**

- Auto-compaction dropped the failing test, both rejected fixes, and the signature
- Auto-compaction points the next step at an unmodified file (refunds/webhook.py)
- The focused /compact summary keeps every fact
- HANDOFF.md keeps every fact

> **Local Jupyter shows `pytest failing: (none)`?** Your kernel is making pytest print colour codes, which break the `^FAILED` regex. Start Jupyter with colour off and rerun: `NO_COLOR=1 jupyter notebook`.

## Done when

Every `check(...)` line prints `PASS`, and the last cell prints `Lab complete.` and a one-line takeaway.

## Getting stuck?

Try each TODO on your own first. Then compare with the finished notebook in [`../solution/`](../solution/README.md), which also lists the complete expected output.
