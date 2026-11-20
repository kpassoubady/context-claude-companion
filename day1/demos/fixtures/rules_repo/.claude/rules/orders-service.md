---
paths:
  - "services/orders/**/*.py"
  - "tests/orders/**/*.py"
---
# Orders Service Rules
- Represent all prices and discounts in integer cents; never use float.
- Require idempotency_key on all order mutation functions.
- Round discounts down; never round in the customer's disfavor.
- Keep pricing functions pure; no I/O inside `services/orders/pricing.py`.
- Verify with: pytest tests/orders -q
