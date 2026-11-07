"""Stateless job payload dispatcher (untouched control module)."""


def validate_job_payload(payload: dict[str, str]) -> tuple[bool, str]:
    """Validate that a job dictionary contains `job_id` and `queue_name`."""
    job_id = payload.get("job_id", "").strip()
    queue_name = payload.get("queue_name", "").strip()
    if not job_id or not queue_name:
        return False, "Missing job_id or queue_name"
    return True, f"{queue_name}:{job_id}"

