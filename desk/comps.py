"""Comparable-company analysis for the Valuation agent."""
from __future__ import annotations

import statistics


def calendarise(fy_values: dict[int, float], fy_end_month: int, target_end_month: int, target_year: int) -> float:
    """Restate a peer's fiscal-year figures onto the 12 months ending in target_end_month of target_year.

    Time-weights the two peer fiscal years that overlap the target period. Fiscal years are
    labelled by the calendar year in which they end. Example: for a December year-end peer and
    Diageo's year to June 2026, the result is 6/12 x FY2025 + 6/12 x FY2026.
    """
    def month_index(year, month):
        return year * 12 + month

    target_end = month_index(target_year, target_end_month)
    # first peer fiscal year ending on or after the target period end
    later_fy = -(-(target_end - fy_end_month) // 12)
    gap = month_index(later_fy, fy_end_month) - target_end  # 0 to 11 months
    if gap == 0:
        return fy_values[later_fy]
    weight_later = (12 - gap) / 12
    return weight_later * fy_values[later_fy] + (1 - weight_later) * fy_values[later_fy - 1]


def implied_values(peer_multiples: list[float], subject_metric: float) -> dict:
    """Median, lowest and highest peer multiples, applied to the subject's metric."""
    clean = sorted(m for m in peer_multiples if m is not None and m > 0)
    if not clean:
        raise ValueError("no usable peer multiples")
    med = statistics.median(clean)
    return {"peers_used": len(clean), "low": clean[0] * subject_metric, "median_multiple": med,
            "implied_value": med * subject_metric, "high": clean[-1] * subject_metric}
