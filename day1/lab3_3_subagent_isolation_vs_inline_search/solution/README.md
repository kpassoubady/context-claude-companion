# Lab 3.3: Subagent Isolation vs. Inline Search (Solution)

Finished, runnable reference for the Lab 3.3 notebook. Run it to see the result without doing the exercise. To do the exercise yourself, start in [`../start/`](../start/README.md).

**Goal:** Measure what lands in the parent context window for a targeted inline search, a broad inline exploration, and the same exploration delegated to a subagent, then check when local `grep` beats an external index.

**Needs:** Python 3.10+, `git`, and `grep` (all present in Colab). No API key. No fixtures: the notebook builds its own service tree.

## Run it

**Option 1: print the results in your terminal** (needs Jupyter, for example `pip install notebook`). From this folder:

```bash
jupyter nbconvert --to markdown --execute --stdout lab3_3_subagent_isolation_vs_inline_search.ipynb
```

This runs every cell and prints each cell's code with its output. To see only the verdicts, filter for the check lines:

```bash
jupyter nbconvert --to markdown --execute --stdout lab3_3_subagent_isolation_vs_inline_search.ipynb 2>/dev/null | grep -E "^ +(PASS|TODO)  "
```

**Option 2: open it.** Run `jupyter notebook lab3_3_subagent_isolation_vs_inline_search.ipynb` and choose **Run > Run All Cells**, or use Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab3_3_subagent_isolation_vs_inline_search/solution/lab3_3_subagent_isolation_vs_inline_search.ipynb)

**Success looks like:** every `check(...)` line prints `PASS` and the last cell prints `Lab complete.`

## What you should see

```text
Targeted inline search: 823 tokens
  defined in: ['services/mod_04/handler.py', 'services/mod_09/handler.py']
  called from: ['services/mod_02/handler.py', 'services/mod_07/handler.py', 'services/mod_11/handler.py']
PASS  Targeted inline search costs 823 tokens
PASS  Two defining modules found
PASS  Three calling modules found

Mode                                               | Parent window | Subagent window | Total model work
--------------------------------------------------------------------------------------------------------
A. Inline, targeted (grep symbol + read 2 files)   |           823 |               0 |              823
B. Inline, broad (read every module that matches)  |         4,404 |               0 |            4,404
C. Subagent, same broad exploration (modeled)      |            67 |           4,404 |            4,471

PASS  Broad inline exploration costs 4,404 tokens
PASS  The subagent's parent window is only 67 tokens
PASS  The subagent still does 4,471 tokens of total model work
PASS  Delegation keeps the parent smaller than even the targeted inline search

Task: callers of `verify_idempotency_token` in this repo
  grep hits: 5 -> local Grep + Read
Task: find an uncommitted edit made after the index was built
  index snapshot hits: 0; grep hits: 1; git diff:  1 file changed, 3 insertions(+)
  -> working tree changes are visible to Grep and git diff, not to an index built earlier
Task: search 4,000 historical postmortems across 15 teams
  grep hits in this repo: 0 -> corpus is not local; use an access-controlled retrieval service (not run here)

PASS  Scenario 1: grep finds all 5 references to the symbol
PASS  Scenario 2: the stale index misses the new edit, grep and git diff see it
PASS  Scenario 3: the postmortem corpus is not on disk

Lab complete.
```

## How to read the result

- **A targeted grep is cheap:** 823 tokens to find 2 definitions and 3 callers.
- **A broad inline exploration is 5x that** (4,404 tokens) and all of it lands in your main window.
- **Delegating the same exploration** leaves the parent with a 67-token report. The subagent's own window still absorbs 4,404 tokens, so total model work is slightly higher (4,471). Delegation protects the parent window; it does not make the work free.
- **Local `grep` and `git diff` see uncommitted edits;** an index built earlier does not. An external index is for corpora that are not on disk.

## Takeaway

Delegate broad exploratory reads to a subagent so the parent keeps a short report. Use direct `Grep` and `git` for local code. Reserve an external index for corpora that are not on disk.
