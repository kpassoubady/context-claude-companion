# Lab 3.2: Compaction and Handoff Verifier (Solution)

Finished, runnable reference for the Lab 3.2 notebook. Run it to see the result without doing the exercise. To do the exercise yourself, start in [`../start/`](../start/README.md).

**Goal:** Audit an unfocused auto-compaction summary, a focused `/compact` summary, and a `HANDOFF.md` against what `git status` and `pytest` report for the repository.

**Needs:** Python 3.10+, `pytest`, and `git`. No API key. Reads `day1/demos/fixtures/compaction_repo/`: run from inside your clone, or in Colab where the first cells clone the repo. The first code cell installs `pytest>=7`.

## Run it

**Option 1: print the results in your terminal** (needs Jupyter, for example `pip install notebook`). From this folder:

```bash
jupyter nbconvert --to markdown --execute --stdout lab3_2_compaction_and_handoff_verifier.ipynb
```

This runs every cell and prints each cell's code with its output. To see only the verdicts, filter for the check lines:

```bash
jupyter nbconvert --to markdown --execute --stdout lab3_2_compaction_and_handoff_verifier.ipynb 2>/dev/null | grep -E "^ +(PASS|TODO)  "
```

**Option 2: open it.** Run `jupyter notebook lab3_2_compaction_and_handoff_verifier.ipynb` and choose **Run > Run All Cells**, or use Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab3_2_compaction_and_handoff_verifier/solution/lab3_2_compaction_and_handoff_verifier.ipynb)

**Success looks like:** every `check(...)` line prints `PASS` and the last cell prints `Lab complete.`

## What you should see

```text
Session summary: Investigated duplicate refund postings in the webhook handler.
Looked at refunds/webhook.py and refunds/ledger.py. Tried a cache for seen keys
and some locking. Next step: finish the fix in refunds/webhook.py and refunds/ledger.py.

=== Ground truth from the repository ===
  git status --porcelain : M refunds/ledger.py
  pytest failing         : tests/test_ledger.py::test_duplicate_delivery_is_not_posted_twice
  signature (ast)        : post_refund(self, order_id: str, amount_cents: int, idempotency_key: str) -> bool
  rejected (transcript)  : ttl_dedupe_cache, global_post_lock

PASS  Only refunds/ledger.py is modified
PASS  One test fails: test_duplicate_delivery_is_not_posted_twice
PASS  The ast signature of post_refund is extracted

Artifact                       | Failing test | Rejected fixes | Signature | Unmodified files named as work
--------------------------------------------------------------------------------------------------------------
1. Unfocused auto-compaction   | False        | 0/2            | False     | refunds/webhook.py
2. Focused /compact summary    | True         | 2/2            | True      | none
3. HANDOFF.md                  | True         | 2/2            | True      | none

PASS  Auto-compaction dropped the failing test, both rejected fixes, and the signature
PASS  Auto-compaction points the next step at an unmodified file (refunds/webhook.py)
PASS  The focused /compact summary keeps every fact
PASS  HANDOFF.md keeps every fact

Lab complete.
```

## How to read the result

- **Ground truth:** only `refunds/ledger.py` is modified, exactly one test fails, and `post_refund` has the signature shown, all read from tools.
- **The automatic summary is the cautionary tale:** it names no failing test, keeps neither rejected fix (`ttl_dedupe_cache`, `global_post_lock`), has no signature, and sends you to `refunds/webhook.py`, a file git shows untouched.
- **The focused `/compact` summary and `HANDOFF.md`** keep the failing test, both rejected fixes, and the signature, and name no untouched file.

## Takeaway

An automatic summary can keep the story and drop the failing test, the rejected fixes, and the signature. Check any summary or `HANDOFF.md` against `git status` and `pytest` before you resume work.
