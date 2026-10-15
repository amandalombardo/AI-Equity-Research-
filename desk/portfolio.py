"""Paper portfolio maths: turn the desk's calls into positions and measure them against the benchmark.

Design agreed by the PM on 15 Oct 2026 (portfolio/portfolio.yaml):
- The fund starts fully invested in the benchmark (a blend of total-return index legs).
- Each SELL call is an active bet: a paper short of the stock, with the same amount added to the stock's
  home index leg. HOLD calls get no active bet.
- No rebalancing: every position is fixed in money at the start and then moves with its total return.

Inputs are total-return growth factors (end value / start value of a dividend-adjusted series, in the
instrument's own currency) and the FX rate (USD per GBP) at the start and at the valuation date.
All money amounts are in pounds (GBP) unless a name ends in _usd.
"""
from __future__ import annotations


def growth_factor(start_value: float, end_value: float) -> float:
    """Total-return growth factor = end / start of a dividend-adjusted price series (1.05 = +5%)."""
    if start_value <= 0:
        raise ValueError("start value must be positive")
    return end_value / start_value


def fx_factor(currency: str, usd_per_gbp_start: float, usd_per_gbp_now: float) -> float:
    """Currency translation into pounds. A USD asset bought with pounds at the start rate and valued back
    into pounds at today's rate gains when the dollar strengthens: factor = start rate / today's rate."""
    if currency == "GBP":
        return 1.0
    if currency == "USD":
        return usd_per_gbp_start / usd_per_gbp_now
    raise ValueError(f"unknown currency {currency!r}: use GBP or USD")


def build_positions(fund_gbp: float, benchmark_weights: dict, bets: list[dict]) -> list[dict]:
    """Starting positions in pounds (negative = short).

    benchmark_weights: {leg name: weight}, summing to 1 (e.g. 75% FTSE 100, 25% S&P 500).
    bets: one per SELL call, {"name", "size" (fraction of fund), "home_leg"}. Each bet shorts the stock
    and puts the same amount into its home index leg, so it is a pure relative bet (stock vs its index)
    and the fund's net exposure stays at 100%."""
    if abs(sum(benchmark_weights.values()) - 1) > 1e-9:
        raise ValueError("benchmark weights must add up to 100%")
    legs = {leg: fund_gbp * w for leg, w in benchmark_weights.items()}
    positions = []
    for bet in bets:
        if bet["home_leg"] not in legs:
            raise ValueError(f"{bet['name']}: home leg {bet['home_leg']!r} is not a benchmark leg")
        amount = fund_gbp * bet["size"]
        legs[bet["home_leg"]] += amount  # proceeds of the short go into the home index
        positions.append({"name": bet["name"], "start_gbp": -amount})
    return [{"name": leg, "start_gbp": v} for leg, v in legs.items()] + positions


def value_positions(positions: list[dict], growth: dict, fx: dict) -> list[dict]:
    """Value each position today: start amount x total-return growth x currency factor.
    For a short (negative amount) a rising stock makes the value more negative, i.e. a loss,
    and the dividends the short seller must pay are included because growth is total return."""
    out = []
    for p in positions:
        now = p["start_gbp"] * growth[p["name"]] * fx[p["name"]]
        out.append({**p, "now_gbp": now, "pnl_gbp": now - p["start_gbp"]})
    return out


def fund_value(valued_positions: list[dict]) -> float:
    """Net asset value = longs minus what is owed on the shorts."""
    return sum(p["now_gbp"] for p in valued_positions)


def benchmark_value(fund_gbp: float, benchmark_weights: dict, growth: dict, fx: dict) -> float:
    """What the same money would be worth held in the benchmark blend, without rebalancing."""
    return sum(fund_gbp * w * growth[leg] * fx[leg] for leg, w in benchmark_weights.items())


def active_return(fund_now: float, benchmark_now: float, start: float) -> float:
    """Active return = fund return minus benchmark return: the value added by the desk's calls."""
    return (fund_now - start) / start - (benchmark_now - start) / start


def relative_return(stock_growth: float, index_growth: float) -> float:
    """Relative performance of a stock against its home index, both in the same currency:
    (1 + stock return) / (1 + index return) - 1. Negative means the stock lagged its index."""
    return stock_growth / index_growth - 1


def call_verdict(call: str, rel: float) -> str:
    """Scorecard: a SELL is working when the stock lags its home index. A HOLD has no active bet."""
    if call == "SELL":
        return "working" if rel < 0 else "not working"
    if call == "BUY":
        return "working" if rel > 0 else "not working"
    return "no bet (HOLD)"
