# FastAPI Service Rules (no paths: frontmatter)
- Test runner: Always use `pytest tests/api -q` (never use unittest).
- Outbound HTTP: Always use `httpx.AsyncClient` for service-to-service calls; `requests` is forbidden.
