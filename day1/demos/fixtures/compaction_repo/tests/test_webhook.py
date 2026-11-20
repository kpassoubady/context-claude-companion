from refunds.ledger import RefundLedger
from refunds.webhook import handle_delivery


def test_delivery_reaches_ledger():
    ledger = RefundLedger()
    assert handle_delivery(ledger, {"order_id": "o-9", "amount_cents": 100, "key": "k-9"}) is True
