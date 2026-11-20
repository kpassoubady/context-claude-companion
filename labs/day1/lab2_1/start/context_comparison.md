# Lab 2.1 Before-and-After Context & Verification Record

Fill every cell from your own run. Nothing here is pre-filled.

## Prediction (write before you run anything, minutes 0-2)
- **Prediction:** TODO (starter state: when Claude Code reads `services/notifications/notifier.py`, which guidance is in context: root `CLAUDE.md`, `AGENTS.md`, `.claude/rules/orders.md`? Why?)

## Environment Provenance
- **Model / CLI Version:** TODO (run `claude --version`, or `N/A` if offline)
- **Observation Source:** TODO (`live` if you ran `/context` yourself, `shared` if you recorded a neighbour's or the instructor's)
- **Memory State:** Lab-scoped / clean workspace
- **Control Component Checked:** `services/notifications/notifier.py`

## Comparison Table

Before = run in `start/` before any edit. After = fresh `claude` session in `start/` after your edits.

| Metric | Before | After |
| :--- | :--- | :--- |
| **Root `CLAUDE.md` Line Count** (`wc -l CLAUDE.md`) | TODO | TODO |
| **`.claude/rules/orders.md` `paths:` Globs** | TODO | TODO |
| **`/context` Memory Files & Rules** (paste the line(s) you saw) | TODO | TODO |
| **Control Read (`services/notifications/`)** (Stretch; `N/A` allowed) | TODO | TODO |
| **Order Pricing Tests (`test_pricing.py`)** | TODO | TODO |
| **Instruction Adherence (Int Cents + Key)** | TODO | TODO |

## Technical Judgment Notes
- **Why the legacy comment inside `services/orders/pricing.py` was rejected:** TODO
- **Why `.claude/rules/` is not a security sandbox:** TODO
