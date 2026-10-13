"""Unit conversions that are easy to get wrong: London prices in pence, USD reporting, US ADRs, US-listed shares in dollars."""
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


def per_share_key(ccy: str) -> str:
    """Which value-per-share figure from dcf.equity_bridge is compared with the share price."""
    return {"GBp": "per_share_gbp_pence", "USD": "per_share_usd"}[ccy]


def share_price_key(ccy: str) -> str:
    """Name of the share-price input in inputs.yaml for this price currency."""
    return {"GBp": "share_price_gbp_pence", "USD": "share_price_usd"}[ccy]
