"""Unit conversions that are easy to get wrong: London prices in pence, USD or EUR reporting, US ADRs, US-listed shares in dollars."""
from __future__ import annotations

PENCE_PER_POUND = 100


def pence_to_pounds(pence: float) -> float:
    """London prices are quoted in pence (GBp). 1 GBP = 100 GBp."""
    return pence / PENCE_PER_POUND


def pounds_to_pence(pounds: float) -> float:
    return pounds * PENCE_PER_POUND


def usd_to_pence(usd: float, usd_per_gbp: float) -> float:
    """Convert a USD per-share amount to pence using a USD-per-GBP rate (e.g. 1.27)."""
    return usd / usd_per_gbp * PENCE_PER_POUND


def adr_to_ordinary(per_adr_value: float, adr_ratio: int) -> float:
    """One Diageo ADR (DEO) represents adr_ratio (=4) ordinary shares, so per-share = per-ADR / ratio."""
    return per_adr_value / adr_ratio


PRICE_CURRENCIES = ("GBp", "USD")


def price_currency(company: dict) -> str:
    """Currency the share price is quoted in, from the brief: GBp (London pence, the default) or USD (US listing)."""
    ccy = company.get("price_currency", "GBp")
    if ccy not in PRICE_CURRENCIES:
        raise ValueError(f"Unknown company.price_currency {ccy!r}: use GBp or USD")
    return ccy


REPORTING_CURRENCIES = ("USD", "EUR", "GBP")


def reporting_currency(company: dict) -> str:
    """Currency the accounts (and so the DCF cash flows) are in, from the brief: USD (the default), EUR or GBP."""
    ccy = company.get("reporting_currency", "USD")
    if ccy not in REPORTING_CURRENCIES:
        raise ValueError(f"Unknown company.reporting_currency {ccy!r}: use USD, EUR or GBP")
    return ccy


def fx_key(reporting_ccy: str) -> str:
    """Name of the FX input that turns a reporting-currency value into pounds: reporting currency per GBP."""
    return f"fx_{reporting_ccy.lower()}_per_gbp"


def money_key(name: str, reporting_ccy: str) -> str:
    """Name of an amount in millions of the reporting currency, e.g. dividends_ex_before_valuation_meur."""
    return f"{name}_m{reporting_ccy.lower()}"


def per_share_key(ccy: str, reporting_ccy: str = "USD") -> str:
    """Which value-per-share figure from dcf.equity_bridge is compared with the share price."""
    if ccy == "GBp":
        return "per_share_gbp_pence"
    if reporting_ccy != ccy:
        raise ValueError(f"A {ccy} share price needs {ccy} reporting, not {reporting_ccy}")
    return f"per_share_{ccy.lower()}"


def share_price_key(ccy: str) -> str:
    """Name of the share-price input in inputs.yaml for this price currency."""
    return {"GBp": "share_price_gbp_pence", "USD": "share_price_usd"}[ccy]
