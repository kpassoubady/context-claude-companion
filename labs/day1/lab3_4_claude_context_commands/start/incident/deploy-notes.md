# Deploy Notes: checkout-api v4.18.0

## Changes

- Added retry-on-timeout around the card authorization call (`authorize_card`). Default: 3 retries, 500 ms fixed delay.
- Upgraded the HTTP client library from 2.9 to 2.11.
- Removed the unused `legacy_receipt` endpoint.

## Review comments (paraphrased)

- Reviewer A: "Retries hold the connection for the whole retry window. Worth a budget?" Author: "Gateway p99 is 300 ms, retries will rarely fire." Not resolved before merge.
- Reviewer B approved with no comments.

## Test evidence

- Unit tests: 412 passed.
- Staging load test: 200 requests per second for 10 minutes, no errors. The staging gateway runs a single replica with `pool.max_connections` set to 10 and a mock authorization service that never times out, so retries never fired.

## Rollback plan

Redeploy v4.17.2. Verified in staging on 2026-10-12.
