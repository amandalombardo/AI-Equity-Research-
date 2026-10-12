"""Market risk measures for the Risk agent: beta, volatility, maximum drawdown.

Inputs are pandas Series of prices indexed by date. Both series must be in the
same units over time (pence for DGE.L, index points for the FTSE 100).
"""
from __future__ import annotations

import math

import pandas as pd

PERIODS_PER_YEAR = {"D": 252, "W": 52, "M": 12}


def returns(prices: pd.Series, freq: str = "D") -> pd.Series:
    """Simple returns at daily (D), weekly (W, Friday close) or monthly (M, month-end close) frequency."""
    prices = prices.dropna().sort_index()
    if freq == "W":
        prices = prices.resample("W-FRI").last()
    elif freq == "M":
        prices = prices.resample("ME").last()
    return prices.pct_change().dropna()


def beta(stock_prices: pd.Series, index_prices: pd.Series, freq: str = "M") -> dict:
    """Regression beta = Cov(stock, index) / Var(index), on aligned returns."""
    df = pd.concat([returns(stock_prices, freq), returns(index_prices, freq)], axis=1, join="inner").dropna()
    df.columns = ["stock", "index"]
    if len(df) < 20:
        raise ValueError(f"only {len(df)} overlapping return observations; need at least 20")
    cov = df["stock"].cov(df["index"])
    var = df["index"].var()
    b = cov / var
    corr = df["stock"].corr(df["index"])
    return {"beta": b, "r_squared": corr ** 2, "observations": len(df), "frequency": freq,
            "start": str(df.index[0].date()), "end": str(df.index[-1].date())}


def annualised_volatility(prices: pd.Series, freq: str = "D") -> float:
    """Standard deviation of returns x sqrt(periods per year)."""
    return returns(prices, freq).std() * math.sqrt(PERIODS_PER_YEAR[freq])


def max_drawdown(prices: pd.Series) -> dict:
    """Largest peak-to-trough fall, with the peak and trough dates."""
    prices = prices.dropna().sort_index()
    running_peak = prices.cummax()
    drawdowns = prices / running_peak - 1
    trough_date = drawdowns.idxmin()
    peak_date = prices.loc[:trough_date].idxmax()
    return {"max_drawdown": float(drawdowns.min()), "peak_date": str(peak_date.date()),
            "trough_date": str(trough_date.date()), "peak_price": float(prices[peak_date]),
            "trough_price": float(prices[trough_date])}
