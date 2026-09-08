"""
Cross Margin health assessment.

Session 3 pivot: Futures API access was confirmed blocked on this account
across three separate endpoint variants (positionInformationV2,
accountInformationV3, futures_coin.accountInformation — all the same
permissions error). Binance's Cross Margin product is authorized and
verified working right now, so the Margin Health Copilot pivots here.

Unlike Session 2's Futures fields (which were a best-effort guess, never
confirmed live), the field names below are copied directly from a real
response captured this session via margin.queryCrossMarginAccountDetails:
  marginLevel, totalAssetOfBtc, totalLiabilityOfBtc, totalNetAssetOfBtc,
  tradeEnabled, transferEnabled, userAssets[] (asset, free, locked,
  borrowed, interest, netAsset)
See fixtures/live_cross_margin_snapshot.json for the captured response.

Thresholds below (margin call ~1.3x, liquidation ~1.1x) are Binance's
long-standing, publicly documented cross-margin levels -- well
established, but not verified against a live *non-zero* account state,
since this account currently carries no debt. Same honest-approximation
treatment as Session 2's maintenance-margin-rate constant.
"""

from typing import TypedDict, Optional

MARGIN_CALL_LEVEL = 1.3
LIQUIDATION_LEVEL = 1.1
WARNING_LEVEL = 1.5


class CrossMarginAccount(TypedDict):
    """Confirmed live shape from margin.queryCrossMarginAccountDetails."""
    marginLevel: str
    totalAssetOfBtc: str
    totalLiabilityOfBtc: str
    totalNetAssetOfBtc: str
    tradeEnabled: bool
    transferEnabled: bool


class CrossMarginAssessment(TypedDict):
    margin_level: float
    has_debt: bool
    status: str  # "no_debt" | "healthy" | "warning" | "margin_call" | "liquidation"
    distance_to_margin_call_pct: Optional[float]
    distance_to_liquidation_pct: Optional[float]
    narrative: str


def analyze_cross_margin(account: CrossMarginAccount) -> CrossMarginAssessment:
    margin_level = float(account["marginLevel"])
    total_liability = float(account["totalLiabilityOfBtc"])
    has_debt = total_liability > 0

    distance_to_margin_call_pct = None
    distance_to_liquidation_pct = None

    if not has_debt:
        status = "no_debt"
        narrative = (
            "No borrowed funds outstanding right now, so there's no "
            "liquidation risk on the margin account. Binance reports margin "
            "level at its no-debt sentinel value rather than a real ratio "
            "in this state."
        )
    else:
        distance_to_margin_call_pct = (margin_level - MARGIN_CALL_LEVEL) / MARGIN_CALL_LEVEL * 100
        distance_to_liquidation_pct = (margin_level - LIQUIDATION_LEVEL) / LIQUIDATION_LEVEL * 100

        if margin_level <= LIQUIDATION_LEVEL:
            status = "liquidation"
            severity = "at or past the liquidation threshold"
        elif margin_level <= MARGIN_CALL_LEVEL:
            status = "margin_call"
            severity = "in margin call territory"
        elif margin_level <= WARNING_LEVEL:
            status = "warning"
            severity = "getting tight"
        else:
            status = "healthy"
            severity = "comfortable"

        narrative = (
            f"Margin level is {margin_level:.2f}x ({severity}). Margin call "
            f"sits around {MARGIN_CALL_LEVEL}x ({distance_to_margin_call_pct:+.1f}% "
            f"away), and forced liquidation around {LIQUIDATION_LEVEL}x "
            f"({distance_to_liquidation_pct:+.1f}% away)."
        )

    return {
        "margin_level": margin_level,
        "has_debt": has_debt,
        "status": status,
        "distance_to_margin_call_pct": (
            round(distance_to_margin_call_pct, 2) if distance_to_margin_call_pct is not None else None
        ),
        "distance_to_liquidation_pct": (
            round(distance_to_liquidation_pct, 2) if distance_to_liquidation_pct is not None else None
        ),
        "narrative": narrative,
    }
