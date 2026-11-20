Focused /compact summary (preserve root cause, rejected fixes, failing test, signature):
- Root cause: refunds/ledger.py appends to postings before checking _seen.
- Rejected: ttl_dedupe_cache (breaks late retries), global_post_lock (fails throughput SLA).
- Failing test: tests/test_ledger.py::test_duplicate_delivery_is_not_posted_twice
- Constraint: keep post_refund(self, order_id: str, amount_cents: int, idempotency_key: str) -> bool
- Only refunds/ledger.py has been edited.
