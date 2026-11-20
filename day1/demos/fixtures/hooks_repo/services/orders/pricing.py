"""Order pricing."""


def apply_discount(amount_cents: int, basis_points: int) -> int:
    """Return the discount in integer cents."""
    return (amount_cents * basis_points) // 10_000
