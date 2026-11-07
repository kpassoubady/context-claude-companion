---
paths:
  - "services/orders/**/*.py"
  - "tests/orders/**/*.py"
---
# Orders Service Rules

- Represent all monetary values (`subtotal_cents`, `discount_cents`, `total_cents`) as integer cents (`int`); never use `float`.
- Every call to `calculate_discounted_total` must require a non-empty `idempotency_key: str` and raise `ValueError` if missing or blank.
- Compute basis-point discounts (`0 <= discount_bps <= 10000`) using integer half-up rounding: `((subtotal_cents * discount_bps) + 5000) // 10000`.
- Verify changes with: `python3 verify_lab.py`

