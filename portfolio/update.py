"""Weekly update of the paper portfolio: fund vs benchmark, each index on its own, and a scorecard per call.

Usage: python -m portfolio.update [--as-of YYYY-MM-DD] [--out runs/portfolio/<date>]

Everything is recomputed from the start date on every run from fresh Yahoo Finance data, so there is
no running total that can drift. The maths is in desk/portfolio.py; this file only fetches data,
lines it up by date and writes the report.

Run it after 21:00 UK time: before then today's US prices are not final, and today's rows are dropped.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

import pandas as pd
import yaml

from desk import data_sources
from desk import portfolio as pf
from desk.rating import rating

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "portfolio" / "portfolio.yaml"


def load_config(path: Path = CONFIG) -> dict:
    cfg = yaml.safe_load(path.read_text())
    for call in cfg["calls"]:
        # the published call and fair value come from the final run, the band thresholds from the brief
        val = json.loads((ROOT / call["run"] / "valuation" / "valuation.json").read_text())["base"]["rating"]
        brief = yaml.safe_load((ROOT / call["brief"]).read_text())
        call["published_call"] = val["rating"]
        # a PM re-rating (e.g. Unilever HOLD -> SELL on 15 Oct 2026) replaces the published call; fair value is unchanged
        call["call"] = call.get("pm_rerating", {}).get("call", val["rating"])
        call["fair_value"] = val["fair_value"]
        call["memo_price"] = val["share_price"]
        call["buy_at"] = brief["rating"]["buy_if_upside_at_least"]
        call["sell_at"] = brief["rating"]["sell_if_downside_at_least"]
    return cfg


def tickers(cfg: dict) -> list[str]:
    return [leg["ticker"] for leg in cfg["benchmark"].values()] + [c["ticker"] for c in cfg["calls"]] + [cfg["fx_ticker"]]


def fetch(cfg: dict, now: dt.datetime | None = None) -> dict[str, pd.DataFrame]:
    """Download each instrument. Today's row is dropped before 21:00 UTC because it is not a final close."""
    now = now or dt.datetime.now(dt.timezone.utc)
    out = {}
    for t in tickers(cfg):
        df = data_sources.daily_closes(t)
        if now.hour < 21:
            df = df[df.index.date < now.date()]
        out[t] = df
    return out


def _on_or_before(df: pd.DataFrame, day: pd.Timestamp) -> pd.Series:
    rows = df[df.index <= day]
    if rows.empty:
        raise RuntimeError(f"MISSING: no price on or before {day.date()}")
    return rows.iloc[-1]


def compute(cfg: dict, data: dict[str, pd.DataFrame], as_of: str) -> dict:
    start, end = pd.Timestamp(cfg["start_date"]), pd.Timestamp(as_of)
    for t, df in data.items():
        if start not in df.index:
            raise RuntimeError(f"MISSING: {t} has no close on the start date {start.date()}; stop and report it")
    fund = cfg["fund_gbp"]
    weights = {leg: v["weight"] for leg, v in cfg["benchmark"].items()}
    sells = [c for c in cfg["calls"] if c["call"] == "SELL"]
    bets = [{"name": c["name"], "size": cfg["bet_size"], "home_leg": c["home_leg"]} for c in sells]
    positions = pf.build_positions(fund, weights, bets)

    ticker_of = {**{leg: v["ticker"] for leg, v in cfg["benchmark"].items()}, **{c["name"]: c["ticker"] for c in cfg["calls"]}}
    ccy_of = {**{leg: v["currency"] for leg, v in cfg["benchmark"].items()}, **{c["name"]: c["currency"] for c in cfg["calls"]}}
    fx_df = data[cfg["fx_ticker"]]
    fx_start = fx_df.loc[start, "close"]

    # one row per trading day (London or New York); a market that was shut keeps its last close
    days = sorted({d for df in data.values() for d in df.index if start <= d <= end})
    daily = []
    for day in days:
        fx_now = _on_or_before(fx_df, day)["close"]
        growth = {n: pf.growth_factor(data[t].loc[start, "adj_close"], _on_or_before(data[t], day)["adj_close"])
                  for n, t in ticker_of.items()}
        fx = {n: pf.fx_factor(ccy_of[n], fx_start, fx_now) for n in ticker_of}
        valued = pf.value_positions(positions, growth, fx)
        f, b = pf.fund_value(valued), pf.benchmark_value(fund, weights, growth, fx)
        daily.append({"date": day.date().isoformat(), "fund_gbp": f, "benchmark_gbp": b,
                      "fund_return": f / fund - 1, "benchmark_return": b / fund - 1,
                      "active_return": pf.active_return(f, b, fund),
                      "ftse100_tr_gbp": growth["ftse100"] - 1,
                      "sp500_tr_usd": growth["sp500"] - 1,
                      "sp500_tr_gbp": growth["sp500"] * fx["sp500"] - 1,
                      "usd_per_gbp": fx_now})

    last = pd.Timestamp(days[-1])
    growth = {n: pf.growth_factor(data[t].loc[start, "adj_close"], _on_or_before(data[t], last)["adj_close"])
              for n, t in ticker_of.items()}
    fx_now = _on_or_before(fx_df, last)["close"]
    fx = {n: pf.fx_factor(ccy_of[n], fx_start, fx_now) for n in ticker_of}
    valued = pf.value_positions(positions, growth, fx)

    scorecard = []
    for c in cfg["calls"]:
        df = data[c["ticker"]]
        latest = _on_or_before(df, last)
        rel = pf.relative_return(growth[c["name"]], growth[c["home_leg"]])
        band = rating(c["fair_value"], latest["close"], c["buy_at"], c["sell_at"])
        scorecard.append({
            "name": c["name"], "call": c["call"], "published_call": c["published_call"], "fair_value": c["fair_value"],
            "unit": "USD" if c["currency"] == "USD" else "GBp",
            "start_price": df.loc[start, "close"], "latest_price": latest["close"],
            "latest_date": latest.name.date().isoformat(),
            "stock_tr": growth[c["name"]] - 1, "index_tr": growth[c["home_leg"]] - 1,
            "home_index": cfg["benchmark"][c["home_leg"]]["label"], "relative": rel,
            "verdict": pf.call_verdict(c["call"], rel),
            "upside_now": band["upside"], "band_now": band["rating"],
            "band_flag": band["rating"] != c["call"],
        })
    price_dates = {t: _on_or_before(df, last).name.date().isoformat() for t, df in data.items()}
    return {"as_of": last.date().isoformat(), "start_date": cfg["start_date"], "fund_gbp": fund,
            "usd_per_gbp_start": fx_start, "usd_per_gbp_now": fx_now,
            "positions": valued, "daily": daily, "scorecard": scorecard, "price_dates": price_dates}


def _pct(x: float) -> str:
    return f"{x * 100:+.2f}%"


def _price(x: float, unit: str) -> str:
    return f"USD {x:,.2f}" if unit == "USD" else f"{x:,.1f}p"


def report(cfg: dict, res: dict) -> str:
    d = res["daily"][-1]
    labels = {leg: v["label"] for leg, v in cfg["benchmark"].items()}
    lines = [
        f"# Paper portfolio update, {res['as_of']}",
        "",
        f"Started {res['start_date']} with GBP {res['fund_gbp']:,.0f}. Student project, not investment advice.",
        "",
        "## Headline",
        "",
        "| | Value (GBP) | Return since start |",
        "|---|---|---|",
        f"| Desk fund | {d['fund_gbp']:,.0f} | {_pct(d['fund_return'])} |",
        f"| Benchmark (75% FTSE 100 / 25% S&P 500, total return) | {d['benchmark_gbp']:,.0f} | {_pct(d['benchmark_return'])} |",
        f"| **Active return (value added by the calls)** | {d['fund_gbp'] - d['benchmark_gbp']:+,.0f} | **{_pct(d['active_return'])}** |",
        "",
        "| Index on its own | Return since start |",
        "|---|---|",
        f"| FTSE 100 total return, GBP | {_pct(d['ftse100_tr_gbp'])} |",
        f"| S&P 500 total return, USD | {_pct(d['sp500_tr_usd'])} |",
        f"| S&P 500 total return, in GBP | {_pct(d['sp500_tr_gbp'])} |",
        "",
        f"FX: USD {res['usd_per_gbp_start']:.4f} per GBP at the start, USD {res['usd_per_gbp_now']:.4f} now (Yahoo {cfg['fx_ticker']}).",
        "",
        "## Scorecard: each call against its home index (own currency, total return)",
        "",
        "| Stock | Call | Stock return | Home index return | Relative | Verdict |",
        "|---|---|---|---|---|---|",
    ]
    for s in res["scorecard"]:
        lines.append(f"| {s['name']} | {s['call']} | {_pct(s['stock_tr'])} | {_pct(s['index_tr'])} | {_pct(s['relative'])} | {s['verdict']} |")
    lines += ["", "## Rating band check (fair value from the final memo vs latest actual price)", "",
              "| Stock | Call | Fair value | Price at start | Latest price | Upside now | Band now | Flag |",
              "|---|---|---|---|---|---|---|---|"]
    for s in res["scorecard"]:
        flag = f"**FLAG: now in {s['band_now']} band; PM to decide whether to re-run**" if s["band_flag"] else "ok"
        lines.append(f"| {s['name']} | {s['call']} | {_price(s['fair_value'], s['unit'])} | {_price(s['start_price'], s['unit'])} | "
                     f"{_price(s['latest_price'], s['unit'])} ({s['latest_date']}) | {_pct(s['upside_now'])} | {s['band_now']} | {flag} |")
    rerated = [f"{c['name']} {c['published_call']} -> {c['call']} ({c['pm_rerating']['date']}: {c['pm_rerating']['reason']})"
               for c in cfg["calls"] if "pm_rerating" in c]
    lines += ["", "Calls stay as published unless the PM re-rates them (design choice 4)."]
    lines += [f"PM re-rating: {r}" for r in rerated]
    lines += ["",
              "## Positions (GBP)", "", "| Position | Start | Now | Profit/loss |", "|---|---|---|---|"]
    for p in res["positions"]:
        name = labels.get(p["name"], f"{p['name']} short")
        lines.append(f"| {name} | {p['start_gbp']:,.0f} | {p['now_gbp']:,.0f} | {p['pnl_gbp']:+,.0f} |")
    lines += ["", "## Sources", "",
              "Yahoo Finance daily chart data (query1.finance.yahoo.com): dividend-adjusted closes for returns, actual closes for prices. "
              "Latest close used per instrument:", ""]
    lines += [f"- {t}: {day}" + (" (FLAG: no close on the update date; last available close used)" if day < res["as_of"] else "")
              for t, day in res["price_dates"].items()]
    lines += ["", "Fair values and calls: each company's final runs/<TICKER>/<date>/valuation/valuation.json. "
              "Band thresholds: briefs/<TICKER>.yaml.", "", "## Missing / not charged", ""]
    lines += [f"- {m}" for m in cfg["missing"]]
    lines.append("- FTSE 100 total return uses an ETF as a proxy, so its annual fee slightly understates the index.")
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--as-of", default=dt.date.today().isoformat())
    ap.add_argument("--out")
    args = ap.parse_args()
    cfg = load_config()
    res = compute(cfg, fetch(cfg), args.as_of)
    out = Path(args.out or ROOT / "runs" / "portfolio" / res["as_of"])
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.md").write_text(report(cfg, res))
    pd.DataFrame(res["daily"]).to_csv(out / "daily.csv", index=False)
    pd.DataFrame(res["scorecard"]).to_csv(out / "scorecard.csv", index=False)
    pd.DataFrame(res["positions"]).to_csv(out / "positions.csv", index=False)
    print((out / "report.md").read_text())


if __name__ == "__main__":
    main()
