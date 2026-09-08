"""
Margin Health Copilot — calculation engine.

Session 1 defines the interface and data contracts only, so Session 2 has
something concrete to build against and Session 3 has something concrete
to verify against a live connection. This module deliberately does not
compute anything yet — see analyze_position() below.
"""

from typing import TypedDict, Literal, Optional


class Position(TypedDict):
    """
    Mirrors what Binance Agent OS's Account (read-only) scope is expected
    to return for one position, per Binance's product docs. UNCONFIRMED
    against a live tool call — see SKILL.md "Data contract".
    """
    symbol: str
    side: Literal["LONG", "SHORT"]
    position_amt: float
    entry_price: float
    leverage: float
    wallet_balance: float
    margin_type: Literal["isolated", "cross"]


class MarketSnapshot(TypedDict):
    """
    Mirrors what Binance Agent OS's Market Data scope is expected to
    return for one symbol. UNCONFIRMED — see SKILL.md "Data contract".
    """
    symbol: str
    mark_price: float
    funding_rate: Optional[float]


class MarginAssessment(TypedDict):
    liquidation_price: Optional[float]
    distance_to_liquidation_pct: Optional[float]
    narrative: str


def analyze_position(position: Position, market: MarketSnapshot) -> MarginAssessment:
    """
    Given one Agentic sub-account position and a current market snapshot,
    return a margin-health assessment.

    NOT YET IMPLEMENTED. Raises NotImplementedError on purpose, per the
    ruleset's anti-hallucination rule (Section 6, #3): a stub must say
    plainly that it isn't real yet rather than silently returning a
    plausible-looking fake number.

    Session 2 implements the real math here:
      1. If the Account scope returns liquidation_price directly, use it.
      2. If not, derive it from position_amt / entry_price / leverage /
         wallet_balance against Binance's published maintenance-margin
         tier table for the symbol (see Research Brief fallback plan).
    """
    raise NotImplementedError(
        "Margin health math lands in Session 2 — see BUILD_ROADMAP.md"
    )
