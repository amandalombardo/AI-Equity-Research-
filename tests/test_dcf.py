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
    # Terminal year (normalised, grows at 2%): sales 123.42, NOPAT 25.65 x 1.02 = 26.163, D&A 6.171, capex 7.4052,
    #   NWC increase only what 2% growth needs: 121 x 0.02 x 0.1 = 0.242 -> FCF 24.6868
    # TV = 24.6868 / (0.09 - 0.02) = 352.6686
    # EV = 18.15/1.09 + 23.34/1.09^2 + TV/1.09^2
    inp = flat_inputs(growth=[0.10, 0.10], cumulative_savings=[10.0, 20.0], tax_rate=0.25, da_pct_sales=0.05,
                      capex_pct_sales=0.06, nwc_pct_sales=0.10, wacc=0.09, terminal_growth=0.02)
    out = dcf.value(inp)
    assert out["rows"][0]["ufcf"] == pytest.approx(18.15)
    assert out["rows"][1]["ufcf"] == pytest.approx(23.34)
    assert out["terminal_year"]["ufcf"] == pytest.approx(24.6868)
    tv = 24.6868 / 0.07
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


def test_mid_year_flat_perpetuity_equals_textbook_value():
    # Mid-year convention: a flat 20 a year forever, each received mid-year, is worth 20 / 0.10 x 1.10^0.5.
    # The terminal value must move half a year too, or the forecast and the perpetuity use different timing.
    assert dcf.value(flat_inputs(mid_year=True))["enterprise_value"] == pytest.approx(200.0 * 1.1 ** 0.5)


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


def growing_inputs(**overrides):
    return flat_inputs(**{**dict(growth=[0.10, 0.10], cumulative_savings=[10.0, 20.0], tax_rate=0.25, da_pct_sales=0.05,
                                 capex_pct_sales=0.06, nwc_pct_sales=0.10, wacc=0.09, terminal_growth=0.02), **overrides})


def test_terminal_capex_override_changes_only_the_terminal_year():
    # Terminal capex 5% instead of 6%: forecast years unchanged; terminal capex 123.42 x 5% = 6.171 (= D&A),
    # so terminal FCF = 26.163 + 6.171 - 6.171 - 0.242 = 25.921
    out = dcf.value(growing_inputs(terminal_capex_pct_sales=0.05))
    assert out["rows"][1]["ufcf"] == pytest.approx(23.34)
    assert out["terminal_year"]["ufcf"] == pytest.approx(25.921)
    assert out["terminal_value"] == pytest.approx(25.921 / 0.07)


def test_implied_ronic_by_hand():
    # Reinvestment = net capex (7.4052 - 6.171) + NWC 0.242 = 1.4762; rate = 1.4762 / 26.163 = 5.642%
    # Return on new investment = g / rate = 2% / 5.642% = 35.45%
    t = dcf.value(growing_inputs())["terminal_year"]
    assert t["reinvestment"] == pytest.approx(1.4762)
    assert t["implied_ronic"] == pytest.approx(0.02 / (1.4762 / 26.163))


def test_capex_for_ronic_round_trip():
    # Capex chosen for a 12% return on new investment must give back exactly 12%:
    # reinvestment = 2% / 12% x 26.163 = 4.3605; capex = 4.3605 - 0.242 + 6.171 = 10.2895 = 8.337% of 123.42
    inp = growing_inputs()
    pct = dcf.capex_pct_for_ronic(inp, 0.12)
    assert pct == pytest.approx((0.02 / 0.12 * 26.163 - 0.242 + 6.171) / 123.42)
    inp.terminal_capex_pct_sales = pct
    assert dcf.value(inp)["terminal_year"]["implied_ronic"] == pytest.approx(0.12)


def test_restructuring_cash_is_deducted_like_debt():
    # 1000 - 200 debt - 30 restructuring cash = 770; / 100 shares = $7.70; / 1.25 = 616p
    out = dcf.equity_bridge(1000, dcf.Bridge(net_debt=200, restructuring_cash=30), 100, 1.25)
    assert out["per_share_gbp_pence"] == pytest.approx(616)


def test_roll_forward_by_hand():
    # Equity 800 at the balance sheet date, cost of equity 10%, a quarter of a year to the valuation date,
    # and a dividend of 5 that went ex in between: 800 x 1.1^0.25 - 5 = 814.2108...
    assert dcf.roll_forward(800, 0.10, 0.25, 5) == pytest.approx(800 * 1.1 ** 0.25 - 5)
    # a buyback after the balance sheet date is cash that left, like a dividend
    assert dcf.roll_forward(800, 0.10, 0.25, 5, buybacks=20) == pytest.approx(800 * 1.1 ** 0.25 - 25)
    # a stake already at today's market price is not grown again
    assert dcf.roll_forward(800, 0.10, 0.25, priced_at_valuation_date=300) == pytest.approx(500 * 1.1 ** 0.25 + 300)
    b = dcf.Bridge(net_debt=200)
    out = dcf.equity_bridge(1000, b, 100, 1.25, {"cost_of_equity": 0.10, "years": 0.25, "dividends": 5})
    assert out["equity_value_balance_sheet_date"] == pytest.approx(800)
    assert out["per_share_usd"] == pytest.approx((800 * 1.1 ** 0.25 - 5) / 100)


def test_sensitivity_rederives_capex_from_ronic():
    # With a RONIC rule, each cell must equal a fresh valuation at that growth with capex set by the rule
    inp = growing_inputs()
    grid = dcf.sensitivity(inp, [0.09], [0.01, 0.02], terminal_ronic=0.12)
    for g, ev in zip([0.01, 0.02], grid[0]):
        trial = growing_inputs(terminal_growth=g)
        trial.terminal_capex_pct_sales = dcf.capex_pct_for_ronic(trial, 0.12)
        assert ev == pytest.approx(dcf.value(trial)["enterprise_value"])


def test_proportionate_minorities_by_hand():
    # Minorities own 5% of operating profit: 5% x EV 1000 = 50 deducted, replacing the book value of 999
    # 1000 - 200 debt - 50 = 750; / 100 shares = $7.50; / 1.25 = 600p
    out = dcf.equity_bridge(1000, dcf.Bridge(net_debt=200, minority_interests=999, minority_share_of_ev=0.05), 100, 1.25)
    assert out["minorities_deducted"] == pytest.approx(50)
    assert out["per_share_gbp_pence"] == pytest.approx(600)
    with pytest.raises(dcf.ValuationError):
        dcf.equity_bridge(1000, dcf.Bridge(net_debt=200, minority_share_of_ev=1.2), 100, 1.25)
