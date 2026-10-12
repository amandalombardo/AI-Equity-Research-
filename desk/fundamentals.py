"""Ratio calculations for the Fundamentals agent.

Each function takes plain numbers (USD m) so Codex can check them by hand.
Functions return None instead of guessing when a denominator is zero or missing.
"""
from __future__ import annotations


def _div(a, b):
    if a is None or b in (None, 0):
        return None
    return a / b


def growth(current, previous):
    """Year-on-year growth = current / previous - 1."""
    r = _div(current, previous)
    return None if r is None else r - 1


def margin(profit, sales):
    """Profit as a share of net sales."""
    return _div(profit, sales)


def roic(operating_profit, tax_rate, invested_capital_open, invested_capital_close):
    """Return on invested capital = NOPAT / average invested capital."""
    if None in (operating_profit, tax_rate, invested_capital_open, invested_capital_close):
        return None
    return _div(operating_profit * (1 - tax_rate), (invested_capital_open + invested_capital_close) / 2)


def cash_conversion(free_cash_flow, net_profit):
    """Free cash flow / net profit attributable to shareholders."""
    return _div(free_cash_flow, net_profit)


def leverage(net_debt, ebitda):
    """Net debt / EBITDA (the company's own target range is 2.5 to 3.0x)."""
    return _div(net_debt, ebitda)


def interest_cover(operating_profit, net_interest_expense):
    """Operating profit / net interest expense."""
    return _div(operating_profit, net_interest_expense)
