# Lab 3.4: Claude Code Context Commands (Solution)

The finished reference for Lab 3.4. Read it and run its check to see the outcome without doing the live session. To do the exercise yourself, start in [`../start/`](../start/README.md).

**Goal:** Measure how much `/context`, `/compact` (plain and focused), `/clear` and `/autocompact` keep, drop and cost, then show with evidence that a short `HANDOFF.md` preserves what a summary does not.

**Needs:** A shell with `git`. No Python and no API key. Claude Code is **not** needed to run this solution's check, because the live-session numbers are already recorded in its files.

## Run it

From the repository root:

```bash
cd labs/day1/lab3_4_claude_context_commands/solution
./check_lab.sh
```

**Success looks like:**

```text
PASS  LAB_LOG.md has no TODO left
PASS  HANDOFF.md has no TODO left
PASS  HANDOFF.md keeps F3 ticket
PASS  HANDOFF.md keeps F3 due date
PASS  HANDOFF.md keeps F1 constraint
PASS  HANDOFF.md keeps F2 rejected approach and reason
PASS  HANDOFF.md names the root-cause error code
ALL LAB 3.4 CHECKS PASSED!
```

For contrast, `./check_lab.sh` in `../start/` prints `FAIL` lines (18 `TODO` lines left in `LAB_LOG.md`, and `HANDOFF.md` missing every fact).

> The script verifies the *written evidence*, not the live Claude session. It also uses `git diff` to confirm `incident/` is unchanged, so run it inside this git checkout. In a plain copy outside a git repository its last check reports `FAIL`.

## What the solution contains

- [`HANDOFF.md`](HANDOFF.md): the safety net. It holds the goal, the root-cause error code (`ERR_POOL_EXHAUSTED_7731`), the three session-only facts, the files that matter, and the next step:
  - **F1:** fixes may only change `checkout-api`; `payment-gw` is out of scope.
  - **F2:** a per-replica pool size of 37 was rejected, because the reporting job holds 12 of the 150 database connections, so 4 x 37 = 148 still exceeds the 138 left.
  - **F3:** ticket `REL-5521`, review due `2026-11-20`.
- [`LAB_LOG.md`](LAB_LOG.md): a filled-in reference log with the baseline and growth readings, the prediction table, the results table, and the reflections.

## What to notice

The reference log shows the pattern you should see in your own session (its numbers are illustrative, and yours will differ with model, plan and Claude Code version):

| Command | What it did to the window | What it did to the facts |
| :--- | :--- | :--- |
| Reading `incident/` | `/context` grew from about 18k to about 33k, mostly Messages | n/a |
| Plain `/compact` | Window fell to about 14k | Kept the gist, **dropped** the reason behind F2 (the reporting job's 12 connections) and the F3 date |
| Focused `/compact <instructions>` | Window fell to about 15k | Kept F1, F2 with its reason, and F3, because the instruction named them |
| `/clear` + `HANDOFF.md` | Window about 19k after rereading the handoff | Kept all of them, read from disk rather than from a summary |

Takeaway: do not trust a summary for facts that were only said in chat. Put them in `HANDOFF.md` or `CLAUDE.md`.

## Replay it live

The solution folder has no `incident/` source files, so replay the session from `../start/`, which has them. Open `claude` there and follow the step-by-step instructions in [`../start/README.md`](../start/README.md). The optional stretch task costs real tokens, so read its warning first.
