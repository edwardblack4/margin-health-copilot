"""
Session 2 test harness. Replaces Session 1's placeholder "not yet
implemented" test with real assertions on the actual margin-health math,
checked against Session 1's mock fixtures. Standard library only — see
Session 1's SESSION_REPORT.md for why pytest was dropped.
"""

import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scripts.margin_health import analyze_position

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "fixtures")


def load_fixture(name):
    with open(os.path.join(FIXTURES, name)) as f:
        return json.load(f)


class TestFixtures(unittest.TestCase):
    def test_account_fixture_shape(self):
        account = load_fixture("mock_account.json")
        self.assertIn("positions", account)
        self.assertEqual(len(account["positions"]), 2)

    def test_market_fixture_shape(self):
        market = load_fixture("mock_market.json")
        self.assertIn("BTCUSDT", market)
        self.assertIn("mark_price", market["BTCUSDT"])


class TestMarginHealthEngine(unittest.TestCase):
    def setUp(self):
        self.account = load_fixture("mock_account.json")
        self.market = load_fixture("mock_market.json")

    def test_long_position_liquidates_below_entry(self):
        position = self.account["positions"][0]  # BTCUSDT LONG
        snapshot = self.market[position["symbol"]]
        result = analyze_position(position, snapshot)
        self.assertIsNotNone(result["liquidation_price"])
        self.assertLess(result["liquidation_price"], position["entry_price"])
        self.assertGreater(result["distance_to_liquidation_pct"], 0)

    def test_short_position_liquidates_above_entry(self):
        position = self.account["positions"][1]  # ETHUSDT SHORT
        snapshot = self.market[position["symbol"]]
        result = analyze_position(position, snapshot)
        self.assertIsNotNone(result["liquidation_price"])
        self.assertGreater(result["liquidation_price"], position["entry_price"])
        self.assertGreater(result["distance_to_liquidation_pct"], 0)

    def test_cross_margin_not_faked(self):
        position = dict(self.account["positions"][0])
        position["margin_type"] = "cross"
        snapshot = self.market[position["symbol"]]
        result = analyze_position(position, snapshot)
        self.assertIsNone(result["liquidation_price"])
        self.assertIn("not calculated here yet", result["narrative"])

    def test_narrative_mentions_symbol_and_scenarios(self):
        position = self.account["positions"][0]
        snapshot = self.market[position["symbol"]]
        result = analyze_position(position, snapshot)
        self.assertIn(position["symbol"], result["narrative"])
        self.assertIn("Scenarios:", result["narrative"])

    def test_deep_adverse_move_triggers_liquidation_flag(self):
        # A 20% adverse move on a 10x BTC long should breach liquidation.
        position = self.account["positions"][0]
        snapshot = self.market[position["symbol"]]
        result = analyze_position(position, snapshot, scenario_pct_moves=[20])
        self.assertIn("trigger liquidation", result["narrative"])


if __name__ == "__main__":
    unittest.main()
