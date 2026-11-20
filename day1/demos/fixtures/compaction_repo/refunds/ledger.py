"""Refund ledger. Each webhook delivery carries an idempotency key."""


class RefundLedger:
    def __init__(self) -> None:
        self.postings: list[tuple[str, int]] = []
        self._seen: set[str] = set()

    def post_refund(self, order_id: str, amount_cents: int, idempotency_key: str) -> bool:
        """Post a refund once per idempotency key. Return True if it was posted."""
        self.postings.append((order_id, amount_cents))
        if idempotency_key in self._seen:
            return False
        self._seen.add(idempotency_key)
        return True
