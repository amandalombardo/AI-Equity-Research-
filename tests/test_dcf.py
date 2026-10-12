"""Hand-calculated checks for the valuation maths. Each expected value is worked out in the comment."""
import math

import pytest

from desk import dcf


def flat_inputs(**overrides):
    # Sales 100, no growth, 20% margin, no tax/D&A/capex/NWC, no savings -> FCF of 20 every year
    base = dict(base_sales=100.0, base_margin=0.20, growth=[0.0, 0.0], cumulative_savings=[0.0, 0.0],
                flow_through=0.5, tax_rate=0.0, da_pct_sales=0.0, capex_pct_sales=0.0, nwc_pct_sales=0.0,
                wacc=0.10, terminal_growth=0.0)
    base.update(overrides)
    return dcf.DcfInputs(**base)


def test_flat_perpetuity_equals_textbook_value():
    # A flat 20 a year forever at 10% is worth 20 / 0.10 = 200, however the years are split
    assert dcf.value(flat_inputs())["enterprise_value"] == pytest.approx(200.0)


def test_growing_case_by_hand():
    # Year 1: sales 110, EBIT 22 + savings 10*0.5 = 27, tax 25% -> NOPAT 20.25
    #         D&A 5.5, capex 6.6, NWC increase 10*0.1 = 1 -> FCF 20.25 + 5.5 - 6.6 - 1 = 18.15
    # Year 2: sales 121, EBIT 24.2 + 20*0.5 = 34.2, NOPAT 25.65, D&A 6.05, capex 7.26, NWC 1.1 -> FCF 23.34
    # TV = 23.34 * 1.02 / (0.09 - 0.02) = 340.0971...
    # EV = 18.15/1.09 + 23.34/1.09^2 + TV/1.09^2
    inp = flat_inputs(growth=[0.10, 0.10], cumulative_savings=[10.0, 20.0], tax_rate=0.25, da_pct_sales=0.05,
                      capex_pct_sales=0.06, nwc_pct_sales=0.10, wacc=0.09, terminal_growth=0.02)
    out = dcf.value(inp)
    assert out["rows"][0]["ufcf"] == pytest.approx(18.15)
    assert out["rows"][1]["ufcf"] == pytest.approx(23.34)
    tv = 23.34 * 1.02 / 0.07
    assert out["terminal_value"] == pytest.approx(tv)
    assert out["enterprise_value"] == pytest.approx(18.15 / 1.09 + 23.34 / 1.09 ** 2 + tv / 1.09 ** 2)
    # implied exit multiple = TV / final-year EBITDA (34.2 + 6.05)
    assert out["implied_exit_ev_ebitda"] == pytest.approx(tv / 40.25)


def test_stub_period_counts_only_remaining_part_of_first_year():
    # Half of year 1 has passed: count 10 of the 20, discounted 0.5 years; year 2 and TV at 1.5 years
    out = dcf.value(flat_inputs(stub_years=0.5))
    expected = 10 / 1.1 ** 0.5 + 20 / 1.1 ** 1.5 + 200 / 1.1 ** 1.5
    assert out["enterprise_value"] == pytest.approx(expected)


def test_mid_year_convention_periods():
    assert dcf.discount_periods(3, 0.0, True) == pytest.approx([0.5, 1.5, 2.5])
    assert dcf.discount_periods(2, 0.25, True) == pytest.approx([0.375, 1.25])


def test_refuses_terminal_growth_at_or_above_wacc():
    with pytest.raises(dcf.ValuationError):
        dcf.value(flat_inputs(terminal_growth=0.10))
    with pytest.raises(dcf.ValuationError):
        dcf.value(flat_inputs(terminal_growth=0.12))


def test_wacc_by_hand():
    # Ke = 4% + 0.8 x 5% = 8%; Kd after tax = 5% x 0.75 = 3.75%; WACC = 0.7 x 8% + 0.3 x 3.75% = 6.725%
    w = dcf.wacc(dcf.WaccInputs(0.04, 0.05, 0.8, 0.05, 0.25, 0.3))
    assert w["cost_of_equity"] == pytest.approx(0.08)
    assert w["wacc"] == pytest.approx(0.06725)


def test_equity_bridge_and_pence_conversion():
    # 1000 - 200 debt - 50 minorities + 100 associates = 850; / 100 shares = $8.50; / 1.25 = GBP 6.80 = 680p
    b = dcf.Bridge(net_debt=200, minority_interests=50, associates=100)
    out = dcf.equity_bridge(1000, b, 100, 1.25)
    assert out["equity_value"] == pytest.approx(850)
    assert out["per_share_gbp_pence"] == pytest.approx(680)


def test_sensitivity_blanks_invalid_cells():
    grid = dcf.sensitivity(flat_inputs(), [0.02, 0.10], [0.0, 0.03])
    assert grid[0][1] is None  # g 3% >= WACC 2%
    assert grid[1][0] == pytest.approx(200.0)
