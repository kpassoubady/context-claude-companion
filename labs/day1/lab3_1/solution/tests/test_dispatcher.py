"""Baseline unit tests for task_queue/dispatcher.py."""

import unittest
from task_queue.dispatcher import validate_job_payload


class TestDispatcher(unittest.TestCase):
    def test_validate_job_payload(self) -> None:
        ok, key = validate_job_payload({"job_id": "42", "queue_name": "settlement"})
        self.assertTrue(ok)
        self.assertEqual(key, "settlement:42")


if __name__ == "__main__":
    unittest.main()

