# TODO: Add YAML frontmatter (`---`) with `paths:` globs targeting:
#   - "services/orders/**/*.py"
#   - "tests/orders/**/*.py"

# Orders Service Rules

- TODO: Specify that all monetary amounts must be represented as integer cents (`int`), never `float`.
- TODO: Specify that `calculate_discounted_total` requires a non-empty `idempotency_key: str` and raises `ValueError` when missing or blank.
- TODO: Specify integer half-up basis-point discount calculation: `((subtotal_cents * discount_bps) + 5000) // 10000`.

