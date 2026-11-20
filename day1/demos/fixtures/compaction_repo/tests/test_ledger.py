from refunds.ledger import RefundLedger


def test_first_delivery_is_posted():
    ledger = RefundLedger()
    assert ledger.post_refund("o-1", 500, "k-1") is True
    assert ledger.postings == [("o-1", 500)]


def test_duplicate_delivery_is_not_posted_twice():
    ledger = RefundLedger()
    ledger.post_refund("o-1", 500, "k-1")
    ledger.post_refund("o-1", 500, "k-1")
    assert ledger.postings == [("o-1", 500)]
