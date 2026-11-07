"""Acceptance tests for services/orders/pricing.py."""

import unittest
from services.orders.pricing import calculate_discounted_total


class TestOrderPricing(unittest.TestCase):
    def test_standard_basis_point_discount_returns_ints(self) -> None:
        result = calculate_discounted_total(10_000, 1_500, idempotency_key="ord-1001")
        self.assertIs(type(result["discount_cents"]), int)
        self.assertIs(type(result["total_cents"]), int)
        self.assertEqual(result["discount_cents"], 1_500)
        self.assertEqual(result["total_cents"], 8_500)
        self.assertEqual(result["idempotency_key"], "ord-1001")

    def test_half_up_basis_point_rounding(self) -> None:
        # 1999 cents * 1250 bps (12.5%) = 249.875 cents -> 250 cents half-up
        result = calculate_discounted_total(1_999, 1_250, idempotency_key="ord-1002")
        self.assertEqual(result["discount_cents"], 250)
        self.assertEqual(result["total_cents"], 1_749)

        # 100 cents * 50 bps (0.5%) = 0.5 cents -> 1 cent half-up
        edge = calculate_discounted_total(100, 50, idempotency_key="ord-1003")
        self.assertEqual(edge["discount_cents"], 1)
        self.assertEqual(edge["total_cents"], 99)

    def test_missing_or_blank_idempotency_key_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            calculate_discounted_total(5_000, 500, idempotency_key="")
        with self.assertRaises(ValueError):
            calculate_discounted_total(5_000, 500, idempotency_key="   ")

    def test_invalid_subtotal_or_bps_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            calculate_discounted_total(-100, 500, idempotency_key="ord-1004")
        with self.assertRaises(ValueError):
            calculate_discounted_total(1_000, 15_000, idempotency_key="ord-1005")


if __name__ == "__main__":
    unittest.main()

