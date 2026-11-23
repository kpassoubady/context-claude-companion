# Checkout Outage Timeline (2026-10-14, all times UTC)

Status: resolved. Owner of the follow-up review: Platform Reliability.

| Time | Event |
| :--- | :--- |
| 13:02 | Deploy `checkout-api` v4.18.0 begins (adds retry-on-timeout to the card authorization call). |
| 13:09 | Deploy finishes. Error rate on `/checkout/confirm` is 0.3 percent (normal). |
| 13:21 | First alert: p95 latency on `/checkout/confirm` above 4 seconds. |
| 13:26 | Error rate reaches 18 percent. Customers see "Payment could not be processed". |
| 13:31 | On-call engineer pages Payments. Incident declared SEV-2. |
| 13:38 | Payments confirms the gateway is healthy; the failures are on our side. |
| 13:44 | `payment-gw` logs show repeated `ERR_POOL_EXHAUSTED_7731` (connection pool exhausted). |
| 13:52 | Retry-on-timeout from v4.18.0 identified as the amplifier: each timed-out call retries three times, holding connections. |
| 14:05 | Mitigation: roll back `checkout-api` to v4.17.2. |
| 14:12 | Error rate returns to 0.4 percent. |
| 14:30 | Incident closed. Follow-up review scheduled. |

## Impact

- Duration of customer impact: 51 minutes (13:21 to 14:12).
- Failed checkouts: about 2,300.
- No double charges were found.

## Open questions for the review

1. Why did the connection pool exhaust at 40 connections when the database allows 150?
2. Should retries be bounded by a shared budget instead of a per-call count?
3. Why did the staging load test not reproduce the pool exhaustion?
