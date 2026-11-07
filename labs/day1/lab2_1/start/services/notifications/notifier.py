"""Notification formatting helper (non-matching control component)."""


def format_order_receipt(order_id: str, total_cents: int) -> str:
    """Format a plain-text receipt summary for an order."""
    if not order_id or not order_id.strip():
        raise ValueError("order_id is required")
    dollars = total_cents // 100
    cents = total_cents % 100
    return f"Order {order_id.strip()}: ${dollars}.{cents:02d} confirmed"

