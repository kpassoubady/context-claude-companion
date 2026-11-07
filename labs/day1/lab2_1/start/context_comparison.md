# Lab 2.1 Before-and-After Context & Verification Record

## Environment Provenance
- **Model / CLI Version:** TODO (record model/CLI version or `N/A` if offline)
- **Memory State:** Lab-scoped / clean workspace
- **Control Component Checked:** `services/notifications/notifier.py`

## Comparison Table

| Metric | Before (Starter Baseline) | After (Refactored & Scoped) |
| :--- | :--- | :--- |
| **Root `CLAUDE.md` Line Count** | 95 lines | TODO |
| **`.claude/rules/orders.md` `paths:` Globs** | Unconfigured (`TODO`) | TODO |
| **Observed `/context` Startup Usage** | Baseline bloated (or `N/A`) | TODO |
| **Control Read (`services/notifications/`)** | All rules loaded at startup | TODO |
| **Order Pricing Tests (`test_pricing.py`)** | FAIL (float output & missing key check) | TODO |
| **Instruction Adherence (Int Cents + Key)** | FAIL (followed legacy float pattern) | TODO |

## Technical Judgment Notes
- **Why the legacy comment inside `services/orders/pricing.py` was rejected:** TODO
- **Why `.claude/rules/` is not a security sandbox:** TODO

