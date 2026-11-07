"""Baseline tests for services/notifications/notifier.py."""

import unittest
from services.notifications.notifier import format_order_receipt


class TestNotifier(unittest.TestCase):
    def test_format_order_receipt(self) -> None:
        self.assertEqual(
            format_order_receipt("ORD-55", 8_505),
            "Order ORD-55: $85.05 confirmed",
        )


if __name__ == "__main__":
    unittest.main()

