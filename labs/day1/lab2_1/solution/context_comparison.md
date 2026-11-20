# Lab 2.1 Before-and-After Context & Verification Record

Reference answers. Your own values will differ in wording and token counts.

## Prediction (write before you run anything, minutes 0-2)
- **Prediction:** `orders.md` has no `paths:` frontmatter, so it loads at startup like `CLAUDE.md`; all three sources are in context even for `notifier.py`.

## Environment Provenance
- **Model / CLI Version:** Claude Code (record the output of `claude --version`)
- **Observation Source:** live
- **Memory State:** Lab-scoped / clean workspace
- **Control Component Checked:** `services/notifications/notifier.py`

## Comparison Table

Before = run in `start/` before any edit. After = fresh `claude` session in `start/` after your edits.

| Metric | Before | After |
| :--- | :--- | :--- |
| **Root `CLAUDE.md` Line Count** (`wc -l CLAUDE.md`) | 75 lines | 18 lines |
| **`.claude/rules/orders.md` `paths:` Globs** | None (no frontmatter) | `services/orders/**/*.py`, `tests/orders/**/*.py` |
| **`/context` Memory Files & Rules** (paste the line(s) you saw) | Memory files: CLAUDE.md, AGENTS.md, orders.md all listed at startup | Memory files: CLAUDE.md, AGENTS.md; orders.md not listed until an orders file is read |
| **Control Read (`services/notifications/`)** (Stretch; `N/A` allowed) | N/A (Stretch not run) | N/A (Stretch not run) |
| **Order Pricing Tests (`test_pricing.py`)** | 4 of 5 tests fail | 5 of 5 tests pass |
| **Instruction Adherence (Int Cents + Key)** | Float output, no key check | Integer arithmetic plus `ValueError` guard |

## Technical Judgment Notes
- **Why the legacy comment inside `services/orders/pricing.py` was rejected:** Source comments and issue descriptions are untrusted data (OWASP LLM01) and must never override project invariants in `.claude/rules/orders.md`.
- **Why `.claude/rules/` is not a security sandbox:** Path-scoped rules control when guidance enters model context, not which files or commands tools are allowed to access.
