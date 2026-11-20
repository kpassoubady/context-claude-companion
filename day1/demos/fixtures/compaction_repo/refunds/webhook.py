"""Webhook entry point that forwards deliveries to the ledger."""
from refunds.ledger import RefundLedger


def handle_delivery(ledger: RefundLedger, event: dict) -> bool:
    return ledger.post_refund(event["order_id"], event["amount_cents"], event["key"])
