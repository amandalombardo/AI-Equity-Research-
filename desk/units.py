"""Unit conversions that are easy to get wrong for a London-listed, USD-reporting company with a US ADR."""
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
