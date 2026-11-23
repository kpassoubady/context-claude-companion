# Task Handoff: Checkout Outage Review

## Goal
Finish the post-incident review of the 2026-10-14 checkout outage (SEV-2, 13:21 to 14:12 UTC, about 2,300 failed checkouts). Answer the three open questions in `incident/timeline.md` and propose a retry-budget design.

## Root cause (from the files)
- Error code: `ERR_POOL_EXHAUSTED_7731` in `incident/payment-gateway.log` (13:44:03Z, 13:52:41Z).
- `checkout-api` v4.18.0 added 3 retries on timeout. Each retry holds a pool connection for the whole window (`incident/deploy-notes.md`).
- Pool max is 40 per replica with 4 replicas (160) against a database limit of 150 (`incident/runbook.md`).

## Session-only facts (not in any file, from the instructor-style briefing)
- F1 constraint: Fixes may only change `checkout-api`. `payment-gw` belongs to Payments and is out of scope.
- F2 rejected approach: Per-replica pool size 37 (150 divided by 4) was rejected. The reporting job holds 12 of the 150 database connections, so 4 x 37 = 148 still exceeds the 138 left.
- F3 tracking: Ticket REL-5521. Review due 2026-11-20.

## Files that matter
- `incident/runbook.md` for pool settings and the capacity arithmetic.
- `incident/deploy-notes.md` for the unresolved reviewer comment on retries.
- `incident/payment-gateway.log` for the two signal lines among routine noise.

## Next step
Draft the retry-budget proposal inside `checkout-api` only, then link it to REL-5521.
