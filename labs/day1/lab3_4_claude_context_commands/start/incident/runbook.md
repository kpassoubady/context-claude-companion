# Runbook: Payment Gateway Connection Pool

Service: `payment-gw` (sidecar to `checkout-api`). Config file: `payment-gw/pool.yaml`.

## Normal settings

| Setting | Value | Notes |
| :--- | ---: | :--- |
| `pool.max_connections` | 40 | Per replica. Four replicas run in production. |
| `pool.acquire_timeout_ms` | 2000 | Callers wait this long for a free connection. |
| `pool.idle_timeout_s` | 60 | Idle connections are closed after this. |
| `db.max_connections` | 150 | Hard limit on the shared database. Not per replica. |

## Capacity arithmetic

Four replicas at 40 connections each is 160, which is above the database limit of 150. The pool was sized before the fourth replica was added and nobody revisited it. This is the reason raising `pool.max_connections` is not a safe fix.

## Symptoms of pool exhaustion

- `ERR_POOL_EXHAUSTED_7731` in `payment-gw` logs.
- p95 latency on `/checkout/confirm` climbs while the gateway itself reports healthy.
- `pool.in_use` equals `pool.max_connections` for more than 30 seconds.

## Standard response

1. Check `pool.in_use` on the dashboard "Payments / Pool".
2. If the cause is a recent deploy, roll the deploy back first.
3. Drain a replica before restarting it: `payment-gw drain --replica <n>`, wait for `in_use` to reach 0, then restart.
4. Never restart all replicas at once.

## Escalation

Payments on-call first. If unreachable after 10 minutes, page the Platform Reliability lead.
