def apply_discount(amount_cents: int, basis_points: int) -> int:
    return (amount_cents * basis_points) // 10_000
