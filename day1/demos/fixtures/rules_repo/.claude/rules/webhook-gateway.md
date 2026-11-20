---
paths:
  - "services/webhook_gateway/**/*.py"
---
# Webhook Gateway Rules
- Verify HMAC-SHA256 signatures before parsing webhook payloads.
- Use exponential backoff with jitter for outbound retries.
- Return 2xx only after the event is durably queued.
- Verify with: pytest tests/webhook_gateway -q
