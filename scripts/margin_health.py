"""
Margin Health Copilot — calculation engine.

Session 1 defined the interface stub. Session 2 implements the real math:
isolated-margin liquidation price, margin ratio, and adverse-scenario
stress-testing, all derived from first principles (not copied from any
external source) and validated against Session 1's mock fixtures.

Known limitation, stated plainly rather than hidden: Binance's real
maintenance-margin requirement is a per-symbol, per-notional-bracket tier
table, not a flat rate. DEFAULT_MAINTENANCE_MARGIN_RATE below is a
documented approximation (the lowest-bracket rate typical of a major pair),
not a live value. Session 3+ should replace it with the real bracket for
the account's actual notional if the live account tool exposes it.
"""

from typing import TypedDict, Literal, Optional, List

DEFAULT_MAINTENANCE_MARGIN_RATE = 0.004  # 0.4% — approximation, see module docstring


class Position(TypedDict):
    """UNCONFIRMED against a live tool call — see SKILL.md 'Data contract'."""
    symbol: str
    side: Literal["LONG", "SHORT"]
    position_amt: float
    entry_price: float
    leverage: float
    wallet_balance: float
    margin_type: Literal["isolated", "cross"]


class MarketSnapshot(TypedDict):
    """UNCONFIRMED against a live tool call — see SKILL.md 'Data contract'."""
    symbol: str
    mark_price: float
    funding_rate: Optional[float]


class MarginAssessment(TypedDict):
    liquidation_price: Optional[float]
    distance_to_liquidation_pct: Optional[float]
    margin_ratio_pct: Optional[float]
    narrative: str


def _liquidation_price(position: Position, mmr: float) -> Optional[float]:
    """
    Isolated-margin liquidation price, derived from first principles:
    liquidation occurs when wallet balance + unrealized PnL equals the
    maintenance margin requirement (notional x mmr).

    Cross-margin isn't handled — it depends on the whole account's shared
    margin pool, not just this position, and faking a number here would be
    actively misleading. Returns None instead.
    """
    if position["margin_type"] != "isolated":
        return None

    amt = position["position_amt"]
    entry = position["entry_price"]
    wallet = position["wallet_balance"]

    if position["side"] == "LONG":
        denom = amt * (1 - mmr)
        return (entry * amt - wallet) / denom if denom else None
    else:  # SHORT
        denom = amt * (1 + mmr)
        return (wallet + entry * amt) / denom if denom else None


def analyze_position(
    position: Position,
    market: MarketSnapshot,
    maintenance_margin_rate: float = DEFAULT_MAINTENANCE_MARGIN_RATE,
    scenario_pct_moves: Optional[List[float]] = None,
) -> MarginAssessment:
    mark = market["mark_price"]
    liq_price = _liquidation_price(position, maintenance_margin_rate)

    distance_pct = None
    if liq_price is not None and mark:
        if position["side"] == "LONG":
            distance_pct = (mark - liq_price) / mark * 100
        else:
            distance_pct = (liq_price - mark) / mark * 100

    notional = abs(position["position_amt"]) * mark
    maint_required = notional * maintenance_margin_rate
    if position["side"] == "LONG":
        unrealized_pnl = (mark - position["entry_price"]) * position["position_amt"]
    else:
        unrealized_pnl = (position["entry_price"] - mark) * abs(position["position_amt"])
    margin_balance = position["wallet_balance"] + unrealized_pnl
    margin_ratio_pct = (
        maint_required / margin_balance * 100 if margin_balance > 0 else None
    )

    narrative = _narrate(
        position, mark, liq_price, distance_pct, margin_ratio_pct,
        scenario_pct_moves or [5, 10, 20],
    )

    return {
        "liquidation_price": round(liq_price, 2) if liq_price is not None else None,
        "distance_to_liquidation_pct": round(distance_pct, 2) if distance_pct is not None else None,
        "margin_ratio_pct": round(margin_ratio_pct, 2) if margin_ratio_pct is not None else None,
        "narrative": narrative,
    }


def _narrate(position, mark, liq_price, distance_pct, margin_ratio_pct, scenario_pct_moves):
    symbol = position["symbol"]
    side = position["side"].lower()
    lines = []

    if liq_price is None:
        lines.append(
            f"{symbol}: cross-margin liquidation depends on the whole account's "
            f"shared margin pool, not just this position — not calculated here yet."
        )
        return " ".join(lines)

    move_word = "drop" if side == "long" else "rise"
    lines.append(
        f"{symbol} {side} at {mark}: liquidation sits around {liq_price:.2f}, "
        f"a {abs(distance_pct):.1f}% {move_word} away."
    )

    if margin_ratio_pct is not None:
        if margin_ratio_pct >= 80:
            severity = "critically close to a margin call"
        elif margin_ratio_pct >= 50:
            severity = "getting tight"
        else:
            severity = "comfortable for now"
        lines.append(
            f"Margin usage is at {margin_ratio_pct:.1f}% of the maintenance "
            f"requirement — {severity}."
        )

    scenario_bits = []
    for pct in scenario_pct_moves:
        if side == "long":
            hypothetical_mark = mark * (1 - pct / 100)
            still_open = hypothetical_mark > liq_price
        else:
            hypothetical_mark = mark * (1 + pct / 100)
            still_open = hypothetical_mark < liq_price
        scenario_bits.append(
            f"a {pct:.0f}% {move_word} to {hypothetical_mark:.2f} would "
            + ("stay open" if still_open else "trigger liquidation")
        )
    lines.append("Scenarios: " + "; ".join(scenario_bits) + ".")

    return " ".join(lines)
