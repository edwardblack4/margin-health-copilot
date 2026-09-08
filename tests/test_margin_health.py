"""
Session 1 test harness.

Validates that the fixtures load and are shaped as expected, and that the
engine's interface contract holds (it must raise NotImplementedError, not
return a silent fake result). Session 2 will replace
test_analyze_position_not_yet_implemented with real assertions once
analyze_position() is actually implemented.

Uses only the standard library — no external dependencies to install or
verify, since this sandbox has no network access to confirm a pytest
install would even work (ruleset Section 6, #9: verify a dependency before
trusting it).
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
        self.assertEqual(account["positions"][0]["symbol"], "BTCUSDT")

    def test_market_fixture_shape(self):
        market = load_fixture("mock_market.json")
        self.assertIn("BTCUSDT", market)
        self.assertIn("mark_price", market["BTCUSDT"])


class TestEngineContract(unittest.TestCase):
    def test_analyze_position_not_yet_implemented(self):
        account = load_fixture("mock_account.json")
        market = load_fixture("mock_market.json")
        position = account["positions"][0]
        snapshot = market[position["symbol"]]
        with self.assertRaises(NotImplementedError):
            analyze_position(position, snapshot)


if __name__ == "__main__":
    unittest.main()
