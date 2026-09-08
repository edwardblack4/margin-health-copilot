"""
Session 3 test harness for the cross-margin pivot.

Tests against three things:
1. The real, live-captured snapshot (proves the engine handles Binance's
   actual no-debt sentinel correctly, not a guess).
2. An illustrative at-risk fixture (clearly labeled non-live) to exercise
   the margin-call branch a zero-debt account can't demonstrate.
3. Constructed boundary values, to check status thresholds directly.
"""

import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scripts.cross_margin_health import analyze_cross_margin

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "fixtures")


def load_fixture(name):
    with open(os.path.join(FIXTURES, name)) as f:
        return json.load(f)


class TestRealLiveSnapshot(unittest.TestCase):
    def test_no_debt_sentinel_handled(self):
        account = load_fixture("live_cross_margin_snapshot.json")
        result = analyze_cross_margin(account)
        self.assertFalse(result["has_debt"])
        self.assertEqual(result["status"], "no_debt")
        self.assertIsNone(result["distance_to_margin_call_pct"])
        self.assertIn("No borrowed funds", result["narrative"])


class TestIllustrativeAtRisk(unittest.TestCase):
    def test_margin_call_status_and_narrative(self):
        account = load_fixture("mock_cross_margin_at_risk.json")
        result = analyze_cross_margin(account)
        self.assertTrue(result["has_debt"])
        self.assertEqual(result["status"], "margin_call")
        self.assertIn("1.25", result["narrative"])
        self.assertLess(result["distance_to_liquidation_pct"], 20)  # close-ish to liq
        self.assertGreater(result["distance_to_liquidation_pct"], 0)  # not past it yet


class TestBoundaryLogic(unittest.TestCase):
    def _account(self, margin_level, liability="1"):
        return {
            "marginLevel": str(margin_level),
            "totalAssetOfBtc": "1",
            "totalLiabilityOfBtc": liability,
            "totalNetAssetOfBtc": "0",
        }

    def test_healthy_above_warning_level(self):
        result = analyze_cross_margin(self._account(2.0))
        self.assertEqual(result["status"], "healthy")

    def test_warning_between_1_3_and_1_5(self):
        result = analyze_cross_margin(self._account(1.4))
        self.assertEqual(result["status"], "warning")

    def test_margin_call_between_1_1_and_1_3(self):
        result = analyze_cross_margin(self._account(1.2))
        self.assertEqual(result["status"], "margin_call")

    def test_liquidation_at_or_below_1_1(self):
        result = analyze_cross_margin(self._account(1.05))
        self.assertEqual(result["status"], "liquidation")

    def test_zero_liability_short_circuits_to_no_debt(self):
        result = analyze_cross_margin(self._account(999, liability="0"))
        self.assertEqual(result["status"], "no_debt")


if __name__ == "__main__":
    unittest.main()
