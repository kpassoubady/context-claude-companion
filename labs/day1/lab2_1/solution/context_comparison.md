# Lab 2.1 Before-and-After Context & Verification Record

## Environment Provenance
- **Model / CLI Version:** Claude Code CLI (or N/A if using offline fallback transcript)
- **Memory State:** Lab-scoped / clean workspace
- **Control Component Checked:** `services/notifications/notifier.py`

## Comparison Table

| Metric | Before (Starter Baseline) | After (Refactored & Scoped) |
| :--- | :--- | :--- |
| **Root `CLAUDE.md` Line Count** | 95 lines | 22 lines |
| **`.claude/rules/orders.md` `paths:` Globs** | Unconfigured (`TODO`) | `services/orders/**/*.py`, `tests/orders/**/*.py` |
| **Observed `/context` Startup Usage** | Baseline bloated (or `N/A`) | Startup trimmed; orders rule loads on demand |
| **Control Read (`services/notifications/`)** | All rules loaded at startup | `.claude/rules/orders.md` stays unloaded |
| **Order Pricing Tests (`test_pricing.py`)** | FAIL (float output & missing key check) | PASS (4/4 tests passing) |
| **Instruction Adherence (Int Cents + Key)** | FAIL (followed legacy float pattern) | PASS (integer arithmetic + `ValueError` guard) |

## Technical Judgment Notes
- **Why the legacy comment inside `services/orders/pricing.py` was rejected:** Source comments and issue descriptions are untrusted data (OWASP LLM01) and must never override project invariants in `.claude/rules/orders.md`.
- **Why `.claude/rules/` is not a security sandbox:** Path-scoped rules control when guidance enters model context, not which files or commands tools are allowed to access.

