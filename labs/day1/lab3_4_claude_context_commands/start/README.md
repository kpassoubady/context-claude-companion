# Lab 3.4: Claude Code Context Commands (`/context`, `/compact`, `/clear`, `/autocompact`) (Start)

> **Short on time, or want to see the finished result first?** Read the reference log and handoff in [`../solution/`](../solution/README.md) and run its check.
>
> **Doing the exercise?** The `TODO` markers are in `LAB_LOG.md` and `HANDOFF.md`. Unlike the other labs, you fill them from what you observe in your own live Claude Code session. Steps 1 to 6 below walk through it.

## 1. Scenario and Goal

Every other lab in this course is checked with Python. This one is checked in a live Claude Code session. You will work through a post-incident review of a checkout outage and use the context commands themselves: watch the window grow with `/context`, compact it two different ways with `/compact`, reset it with `/clear` and a `HANDOFF.md`, and look at the auto-compaction setting with `/autocompact`.

The three facts you need to protect are told to Claude in chat only. They are in no file. That makes them exactly the kind of state a summary can lose.

**Goal:** Measure how much each command keeps, drops, and costs, then show with evidence that a short `HANDOFF.md` preserves what a summary does not.

---

## 2. Learning Objectives

- Read `/context` before and after a task and explain where the tokens went.
- Run a plain `/compact` and a focused `/compact <instructions>` on the same history and compare what each kept.
- Predict, then test, which session-only facts survive a summary.
- Use `/clear` plus a durable `HANDOFF.md` to resume with explicit state and a small window.
- Explain what `/autocompact` and `--autocompact` control, and why auto-compaction fires without you asking.

---

## 3. Time Budget & Run of Show (25 Minutes)

Work in pairs. Each person runs their **own** Claude Code session in their **own** terminal, so you can compare. The only difference: **Terminal A uses plain `/compact`, Terminal B uses focused `/compact`.** Everything else is identical.

| Minutes | Phase | Required Activity |
| :--- | :--- | :--- |
| **0–3** | Baseline | Start Claude, run `/context`, look at `/autocompact`. Fill `LAB_LOG.md` section 1, row 1. |
| **3–8** | Grow | Have Claude read `incident/`, then run `/context` again. |
| **8–12** | Plant and protect | Tell Claude the three session-only facts, then have it write `HANDOFF.md`. Write your prediction (section 2 of the log). |
| **12–18** | Compact | Terminal A: plain `/compact`. Terminal B: focused `/compact`. Quiz your session, run `/context`, record results. |
| **18–22** | Clear and resume | In either terminal: `/clear`, resume from `HANDOFF.md`, quiz again, run `/context`. |
| **22–25** | Auto-compact, usage, debrief | `/autocompact`, `/usage`, section 4 and 5 of the log, run `./check_lab.sh`. |

> **Pacing Fallback (Minute 18):** If you are behind, skip the plain/focused split. Both terminals run the focused `/compact`, and you compare only against `/clear` + `HANDOFF.md`.

---

## 4. Setup and Starting Commands

You need Claude Code and a terminal. No Python is used.

```bash
cd labs/day1/lab3_4_claude_context_commands/start
./check_lab.sh        # expect FAIL lines: that is your starting point
claude                # start a fresh session in this folder
```

Inside Claude Code:

```text
/context
```

Record the numbers in `LAB_LOG.md`. Then open the auto-compact setting without changing it:

```text
/autocompact
```

Note the current value, then press `Esc` to leave it as it is.

> **Version note:** Slash commands change between Claude Code releases. If `/autocompact` is not recognized in your version, run `claude --help` and look for the `--autocompact` flag, or check `/help`. Record which route you used.

---

## 5. Files You May Change

| File | Action Allowed | Constraints to Preserve |
| :--- | :--- | :--- |
| `LAB_LOG.md` | Edit & complete | Replace every `TODO` with something you observed. |
| `HANDOFF.md` | Create content (have Claude write it, then correct it) | Must carry F1, F2, F3 and the error code. |
| `incident/**` | **Do NOT edit** | Source material. `check_lab.sh` flags any change. |
| `check_lab.sh`, `make_bulk.sh` | **Do NOT edit** | Part of the check. |

---

## 6. Step-by-Step Tasks

### Step 1: Baseline (Minutes 0–3)

Run `/context` in a fresh session. Record total used and the biggest category. Open `/autocompact`, note the window, and leave it unchanged.

### Step 2: Grow the Context (Minutes 3–8)

Paste:

```text
Read every file in incident/ and answer in short bullets, citing the file for each point:
1. What was the root cause and its error code?
2. Why did a pool of 40 exhaust when the database allows 150?
3. What did the staging load test miss?
```

Run `/context` again. Record the growth and which category grew.

### Step 3: Plant the Session-Only Facts and Protect Them (Minutes 8–12)

Paste these exactly as written. They are not in any file.

```text
Three facts for this review, from the Payments sync. Acknowledge them in one line each:
F1. Any fix may only change checkout-api. payment-gw belongs to Payments and is out of scope.
F2. We already rejected a per-replica pool size of 37 (150 divided by 4). The reporting job holds 12 of the 150 database connections, so 4 x 37 = 148 still exceeds the 138 left.
F3. Tracking ticket is REL-5521 and the review is due 2026-11-20.
```

Then ask Claude to write the safety net:

```text
Write HANDOFF.md with: the goal, the root-cause error code, F1, F2 (with its reason), F3, the files that matter, and the next step. Replace the placeholder text. Do not edit anything in incident/.
```

Read `HANDOFF.md` yourself and correct anything wrong. **Before you compact**, fill section 2 of `LAB_LOG.md` (your prediction).

### Step 4: Compact Two Ways (Minutes 12–18)

**Terminal A (plain):**

```text
/compact
```

**Terminal B (focused):**

```text
/compact Keep verbatim: constraint F1, rejected approach F2 with its reason, ticket and due date F3, the error code ERR_POOL_EXHAUSTED_7731, and the three open review questions.
```

Write your own focus text if you prefer, and record exactly what you used. Then, in each terminal, **without letting Claude read any file**, ask:

```text
From memory only, without reading any file: state F1, F2 with its reason, F3, and the root-cause error code.
```

Run `/context` and fill the first two result columns.

### Step 5: Clear and Resume from Disk (Minutes 18–22)

In either terminal:

```text
/clear
```

Run `/context` and note how small the window is. Then:

```text
Read CLAUDE.md and HANDOFF.md. State F1, F2 with its reason, F3, and the root-cause error code. Tell me what is still missing and which file you would read next.
```

Run `/context` again and fill the third result column.

### Step 6: Auto-Compaction and Usage (Minutes 22–25)

1. Run `/autocompact` again. Write one sentence on what it controls (section 4).
2. Run `/usage` and record what it shows.
3. Run `./check_lab.sh` in a normal shell. It should print `ALL LAB 3.4 CHECKS PASSED!`.

> **Careful:** `/autocompact <value>` is saved for the current model and persists after the session. To try a value without leaving it behind, launch a session with `claude --autocompact 100k` instead, or run `/autocompact auto` afterwards to restore the default.

### Human Judgment Checkpoint

Before you trust any compaction summary, ask: if this fact were wrong or missing, what would a fresh session do next? For F2, the answer is propose pool size 37 again.

---

## 7. Completion Levels

- **Basic (Required):** `LAB_LOG.md` is fully filled from your own session, `HANDOFF.md` carries F1, F2, F3 and the error code, and `./check_lab.sh` passes.
- **Intermediate:** Your focus instruction in section 3 is different from the one given, and you can say what changed in the result.
- **Stretch (costs real tokens):** Trigger a live auto-compaction. Run `./make_bulk.sh` (about 400 KB of log noise in `bulk/`, ignored by git), start `claude --autocompact 100k`, and ask Claude to read all of `bulk/`. Write down exactly what you see when compaction fires, then ask for F1 to F3 again.

---

## 8. Definition of Done & Share-Out

Your exercise is complete when `./check_lab.sh` prints `ALL LAB 3.4 CHECKS PASSED!`.

**Group Share-Out (1 minute):**
1. Which fact did plain `/compact` lose or distort, and how did you find out?
2. What did your focus instruction change?
3. Which fact would you now put in `HANDOFF.md` or `CLAUDE.md` instead of trusting a summary?

---

## 9. Troubleshooting & Help

1. If `check_lab.sh` reports a missing fact, open `HANDOFF.md` and add it. The check looks for `REL-5521`, `2026-11-20`, the words `out of scope`, `reporting` with `37`, and `ERR_POOL_EXHAUSTED_7731`.
2. If a TODO remains, `check_lab.sh` prints how many lines are left in `LAB_LOG.md`.
3. If Claude edited a file in `incident/`, run `git checkout -- incident` and ask again with "do not edit incident/".
4. If your numbers differ from a neighbor's, that is expected. Model, version and plan change counts. Compare the pattern, not the number.
5. Compare with `../solution/` only after your own attempt. Its numbers are illustrative.
