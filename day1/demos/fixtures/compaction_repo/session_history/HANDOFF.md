# Handoff: refund idempotency
- Modified files: refunds/ledger.py
- Root cause: post_refund appends to postings before it checks _seen.
- Constraint: keep post_refund(self, order_id: str, amount_cents: int, idempotency_key: str) -> bool
- Failing test: tests/test_ledger.py::test_duplicate_delivery_is_not_posted_twice
- Rejected approaches: ttl_dedupe_cache (breaks late retries); global_post_lock (fails throughput SLA)
- Next: move the append below the _seen check, then run `pytest -q`.
