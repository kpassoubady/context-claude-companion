# Task Queue Worker Service (`task_queue`)

## Architecture & Invariants
- `task_queue/lease.py`: Optimistic sequence-based lease manager (`LeaseManager`).
- `task_queue/dispatcher.py`: Stateless job payload validator and router (must remain unmodified during lease fixes).
- Preserve `LeaseManager.renew_lease(self, lease_id: str, worker_id: str, expected_seq: int) -> dict` signature and `default_ttl_seconds = 30`.
- Never add blocking locks (`threading.Lock`) or modify `default_ttl_seconds` to work around stale lease renewals.

## Verification Commands
- Full lab check: `python3 verify_lab.py`
- Unit tests: `python3 -m unittest discover -s tests -p "test_*.py"`

