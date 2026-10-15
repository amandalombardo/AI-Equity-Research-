"""Paper portfolio: positions, returns and scorecard checked against answers worked out by hand."""
import copy

import pandas as pd
import pytest

from desk import portfolio as pf
from portfolio import update

WEIGHTS = {"ftse100": 0.75, "sp500": 0.25}
BETS = [{"name": "KO", "size": 0.10, "home_leg": "sp500"}, {"name": "RELX", "size": 0.10, "home_leg": "ftse100"}]


def test_positions_start_as_benchmark_plus_one_short_per_sell():
    pos = {p["name"]: p["start_gbp"] for p in pf.build_positions(100_000, WEIGHTS, BETS)}
    # 75,000 FTSE + 10,000 from the RELX short; 25,000 S&P + 10,000 from the KO short
    assert pos == {"ftse100": 85_000, "sp500": 35_000, "KO": -10_000, "RELX": -10_000}
    assert sum(pos.values()) == 100_000  # net exposure stays at the fund size


def test_weights_must_add_up():
    with pytest.raises(ValueError):
        pf.build_positions(100_000, {"ftse100": 0.7, "sp500": 0.25}, [])


def test_short_loses_when_the_stock_rises():
    pos = [{"name": "RELX", "start_gbp": -10_000}]
    v = pf.value_positions(pos, {"RELX": 1.10}, {"RELX": 1.0})[0]
    assert v["now_gbp"] == pytest.approx(-11_000)
    assert v["pnl_gbp"] == pytest.approx(-1_000)


def test_usd_position_gains_when_the_dollar_strengthens():
    # bought at USD 1.30 per GBP, now USD 1.25: each dollar buys more pounds back
    assert pf.fx_factor("USD", 1.30, 1.25) == pytest.approx(1.04)
    assert pf.fx_factor("GBP", 1.30, 1.25) == 1.0


def test_fund_beats_benchmark_by_the_relative_moves_of_the_shorts():
    # by hand: FTSE +2%, S&P +4% (USD), GBP/USD unchanged, RELX -8%, KO +1%
    growth = {"ftse100": 1.02, "sp500": 1.04, "RELX": 0.92, "KO": 1.01}
    fx = {k: 1.0 for k in growth}
    valued = pf.value_positions(pf.build_positions(100_000, WEIGHTS, BETS), growth, fx)
    fund = pf.fund_value(valued)
    bench = pf.benchmark_value(100_000, WEIGHTS, growth, fx)
    # fund = 85,000x1.02 + 35,000x1.04 - 10,000x0.92 - 10,000x1.01 = 103,800
    assert fund == pytest.approx(103_800)
    # benchmark = 75,000x1.02 + 25,000x1.04 = 102,500
    assert bench == pytest.approx(102_500)
    # active = RELX bet (2% - -8%) x 10% + KO bet (4% - 1%) x 10% = 1.0% + 0.3%
    assert pf.active_return(fund, bench, 100_000) == pytest.approx(0.013)


def test_scorecard_relative_return_and_verdicts():
    assert pf.relative_return(0.92, 1.02) == pytest.approx(0.92 / 1.02 - 1)
    assert pf.call_verdict("SELL", -0.05) == "working"
    assert pf.call_verdict("SELL", 0.05) == "not working"
    assert pf.call_verdict("HOLD", 0.05) == "no bet (HOLD)"
    assert pf.call_verdict("SELL", 0.0) == "level with index"  # start day: no move yet, not "not working"


def test_config_reads_the_published_calls():
    cfg = update.load_config()
    calls = {c["name"]: c["call"] for c in cfg["calls"]}
    assert calls == {"DGE": "HOLD", "KO": "SELL", "ULVR": "SELL", "RELX": "SELL"}
    ulvr = next(c for c in cfg["calls"] if c["name"] == "ULVR")
    assert ulvr["published_call"] == "HOLD"  # the memo still says HOLD; the re-rating is the PM's, recorded with a date
    assert sum(leg["weight"] for leg in cfg["benchmark"].values()) == pytest.approx(1.0)
    assert cfg["start_date"] == "2026-10-15"


def _frame(values, dates):
    return pd.DataFrame({"adj_close": values, "close": values}, index=pd.to_datetime(dates))


def _fake(cfg):
    days = ["2026-10-15", "2026-10-16", "2026-10-19"]
    data = {
        "CUKX.L": _frame([100, 101, 102], days),
        "^SP500TR": _frame([100, 103, 104], days),
        "DGE.L": _frame([1740, 1750, 1760], days),
        "KO": _frame([90, 91, 91.80], days[:2] + ["2026-10-19"]),
        "ULVR.L": _frame([4900, 4900, 4900], days),
        "REL.L": _frame([2800, 2700, 2576], days),
        "GBPUSD=X": _frame([1.30, 1.30, 1.30], days),
    }
    return data


def test_compute_end_to_end_on_made_up_prices():
    cfg = update.load_config()
    res = update.compute(cfg, _fake(cfg), "2026-10-19")
    last = res["daily"][-1]
    # FTSE +2%, S&P +4%, RELX 2576/2800 = -8%, KO 91.80/90 = +2%, FX flat
    # three SELL bets: RELX and Unilever (PM re-rated) into the FTSE leg, KO into the S&P leg
    assert last["fund_gbp"] == pytest.approx(95_000 * 1.02 + 35_000 * 1.04 - 10_000 * 0.92 - 10_000 * 1.02 - 10_000 * 1.0)
    assert last["benchmark_gbp"] == pytest.approx(102_500)
    score = {s["name"]: s for s in res["scorecard"]}
    assert score["RELX"]["verdict"] == "working"
    assert score["KO"]["relative"] == pytest.approx(1.02 / 1.04 - 1)
    # Unilever at 4,900p vs 4,258.5p fair value is in the SELL band, matching the PM's re-rating: no flag
    assert score["ULVR"]["band_now"] == "SELL" and not score["ULVR"]["band_flag"]
    assert "PM re-rating: ULVR HOLD -> SELL" in update.report(cfg, res)
    # Diageo at 1,760p vs 1,780.2p stays HOLD; a fall to 1,500p would be flagged as a BUY-band crossing
    data = _fake(cfg)
    data["DGE.L"] = _frame([1740, 1600, 1500], ["2026-10-15", "2026-10-16", "2026-10-19"])
    score = {s["name"]: s for s in update.compute(cfg, data, "2026-10-19")["scorecard"]}
    assert score["DGE"]["band_now"] == "BUY" and score["DGE"]["band_flag"]
    assert "FLAG: now in BUY band" in update.report(cfg, update.compute(cfg, data, "2026-10-19"))


def test_missing_start_price_stops_the_run():
    cfg = update.load_config()
    data = _fake(cfg)
    data["KO"] = data["KO"].iloc[1:]
    with pytest.raises(RuntimeError, match="MISSING"):
        update.compute(cfg, data, "2026-10-19")


def test_a_market_holiday_keeps_the_last_close():
    cfg = copy.deepcopy(update.load_config())
    data = _fake(cfg)
    data["^SP500TR"] = data["^SP500TR"].drop(pd.Timestamp("2026-10-19"))
    res = update.compute(cfg, data, "2026-10-19")
    assert res["daily"][-1]["sp500_tr_usd"] == pytest.approx(0.03)
    assert res["price_dates"]["^SP500TR"] == "2026-10-16"


def test_exchange_cross_check_flags_a_gap_and_never_fills_a_missing_close():
    rows = [{"ticker": "ULVR.L", "date": "2026-10-15", "yahoo": 4915.5, "exchange": 4915.5},
            {"ticker": "KO", "date": "2026-10-15", "yahoo": 92.20, "exchange": 91.50},
            {"ticker": "CUKX.L", "date": "2026-10-14", "yahoo": 22140.0, "exchange": None}]
    out = {r["ticker"]: r for r in update.compare_closes(rows)}
    assert out["ULVR.L"]["status"] == "match"
    assert out["KO"]["status"].startswith("FLAG")  # 0.77% apart
    assert out["CUKX.L"]["diff"] is None and out["CUKX.L"]["status"].startswith("not checked")
