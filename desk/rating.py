"""Apply the PM's rating rule (from the brief YAML) to a fair value and share price."""
from __future__ import annotations


def rating(fair_value: float, share_price: float, buy_if_upside_at_least: float,
           sell_if_downside_at_least: float) -> dict:
    """Upside = fair value / price - 1. Buy at or above the buy threshold, Sell at or below
    minus the sell threshold, Hold in between. Both values must be in the same units (pence)."""
    if share_price <= 0:
        raise ValueError("share price must be positive")
    # rounded so a value exactly on a threshold (e.g. 115 vs 100) isn't misclassified by floating-point error
    upside = round(fair_value / share_price - 1, 10)
    if upside >= buy_if_upside_at_least:
        call = "BUY"
    elif upside <= -sell_if_downside_at_least:
        call = "SELL"
    else:
        call = "HOLD"
    return {"rating": call, "upside": upside, "fair_value": fair_value, "share_price": share_price}
