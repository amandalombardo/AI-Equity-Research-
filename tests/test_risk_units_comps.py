import numpy as np
import pandas as pd
import pytest

from desk import comps, fundamentals, risk, units
from desk.rating import rating


def test_beta_recovers_known_value():
    rng = np.random.default_rng(0)
    dates = pd.bdate_range("2021-01-01", periods=1300)
    idx_ret = rng.normal(0, 0.01, len(dates))
    index = pd.Series(100 * np.cumprod(1 + idx_ret), index=dates)
    # stock returns are exactly 1.2 x index returns -> beta 1.2 at daily frequency
    stock = pd.Series(100 * np.cumprod(1 + 1.2 * idx_ret), index=dates)
    assert risk.beta(stock, index, "D")["beta"] == pytest.approx(1.2)


def test_max_drawdown_known_series():
    s = pd.Series([100, 120, 90, 130, 65, 80], index=pd.date_range("2024-01-01", periods=6))
    out = risk.max_drawdown(s)
    assert out["max_drawdown"] == pytest.approx(-0.5)  # 130 -> 65
    assert out["peak_date"] == "2024-01-04" and out["trough_date"] == "2024-01-05"


def test_volatility_annualisation():
    s = pd.Series([100, 110, 99, 108.9], index=pd.bdate_range("2024-01-01", periods=4))
    r = s.pct_change().dropna()
    assert risk.annualised_volatility(s) == pytest.approx(r.std() * np.sqrt(252))


def test_pence_and_adr_conversions():
    assert units.pence_to_pounds(2150) == pytest.approx(21.50)
    assert units.usd_to_pence(27.0, 1.35) == pytest.approx(2000.0)
    assert units.adr_to_ordinary(100.0, 4) == pytest.approx(25.0)


def test_calendarise_to_june_year_end():
    # December year-end peer: Jul 2025 - Jun 2026 = half of FY2025 + half of FY2026
    assert comps.calendarise({2025: 100, 2026: 200}, 12, 6, 2026) == pytest.approx(150)
    # June year-end peer: no adjustment
    assert comps.calendarise({2026: 123}, 6, 6, 2026) == pytest.approx(123)
    # March year-end peer: Jul 2025 - Mar 2026 (9 months of FY2026) + Apr - Jun 2026 (3 months of FY2027)
    assert comps.calendarise({2026: 100, 2027: 140}, 3, 6, 2026) == pytest.approx(110)
    # April year-end peer (Brown-Forman): 10 months of FY2026 + 2 months of FY2027
    assert comps.calendarise({2026: 120, 2027: 180}, 4, 6, 2026) == pytest.approx(130)


def test_implied_values_uses_median():
    out = comps.implied_values([10, 12, 30, None, -5], 100)
    assert out["median_multiple"] == 12 and out["implied_value"] == 1200 and out["peers_used"] == 3


def test_fundamentals_return_none_not_guesses():
    assert fundamentals.leverage(20500, 0) is None
    assert fundamentals.growth(110, 100) == pytest.approx(0.10)
    assert fundamentals.roic(100, 0.25, 500, 700) == pytest.approx(0.125)


@pytest.mark.parametrize("fair,price,expected", [(115, 100, "BUY"), (114.9, 100, "HOLD"),
                                                  (90, 100, "SELL"), (90.1, 100, "HOLD")])
def test_rating_thresholds(fair, price, expected):
    assert rating(fair, price, 0.15, 0.10)["rating"] == expected
