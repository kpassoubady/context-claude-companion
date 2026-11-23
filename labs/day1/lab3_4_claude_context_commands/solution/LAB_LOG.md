# Lab Log: Claude Code Context Commands (reference example)

These numbers are illustrative. Your counts will differ with your model, plan and Claude Code version. What matters is the pattern: growth after reading, loss after plain compaction, recovery from disk.

## 1. Baseline and growth (`/context`)

| Moment | Command | Total used | Biggest category | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Fresh session | `/context` | about 18k | System prompt and tools | `CLAUDE.md` shows as a small memory file |
| After reading `incident/` | `/context` | about 33k | Messages | The log file is the largest single read |

Auto-compact window shown by `/autocompact` (Step 1): auto (model default, far above this lab's usage)

## 2. Prediction (write BEFORE you compact)

| Fact | Plain `/compact` | Focused `/compact` | `/clear` + `HANDOFF.md` |
| :--- | :--- | :--- | :--- |
| F1 constraint | Unsure | Kept | Kept |
| F2 rejected approach and reason | Lost | Kept | Kept |
| F3 ticket and due date | Unsure | Kept | Kept |

## 3. Result (after each command)

| Check | Plain `/compact` | Focused `/compact` | `/clear` + `HANDOFF.md` |
| :--- | :--- | :--- | :--- |
| F1 constraint recalled correctly? | Yes, paraphrased | Yes | Yes |
| F2 rejected approach and reason recalled? | Approach yes, reason (reporting job, 12 connections) missing | Yes | Yes |
| F3 ticket and due date recalled? | Ticket yes, date missing | Yes | Yes |
| Error code recalled without re-reading? | Yes | Yes | No, it had to re-read the log (it is in `HANDOFF.md` too) |
| `/context` total used afterwards | about 14k | about 15k | about 19k |

The exact focus instruction you used for the focused run:

> /compact Keep verbatim: constraint F1, rejected approach F2 with its reason, ticket and due date F3, the error code ERR_POOL_EXHAUSTED_7731, and the three open review questions.

## 4. Auto-compaction and usage

- What `/autocompact` (or `--autocompact`) lets you change: the token size of the window at which Claude Code compacts on its own (`auto` or at least 100k).
- Why a smaller window triggers compaction sooner: the threshold is a token count, so a lower number is reached after fewer turns.
- `/usage` after the lab: a few dozen turns and a small session cost.

## 5. Reflection (two sentences each)

- What did plain `/compact` get wrong or drop? It kept the gist but dropped the reason behind the rejected pool size and the due date. A fresh session would likely re-propose 37.
- Which fact would you put in `HANDOFF.md` or `CLAUDE.md` instead of trusting a summary, and why? The F2 rejection with its reason, because a lost "why" lets a rejected idea come back.
