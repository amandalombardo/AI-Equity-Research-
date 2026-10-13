"""DCF valuation engine.

All maths for the Valuation and Bear case agents lives here, so the numbers come
from fixed formulas that can be audited (by Codex) and matched to Excel (by the PM).
The AI agents call these functions; they never do valuation arithmetic themselves.

Units: money in USD millions, rates as decimals (0.05 = 5%), shares in millions.
"""
from __future__ import annotations

from dataclasses import dataclass, field


class ValuationError(ValueError):
    """Raised when inputs make the valuation meaningless (e.g. growth >= WACC)."""


@dataclass
class WaccInputs:
    risk_free: float
    equity_risk_premium: float
    beta: float
    pre_tax_cost_of_debt: float
    tax_rate: float
    debt_weight: float  # D / (D + E), market values


def cost_of_equity(risk_free: float, beta: float, equity_risk_premium: float) -> float:
    """CAPM: Ke = Rf + beta x ERP."""
    return risk_free + beta * equity_risk_premium


def wacc(w: WaccInputs) -> dict:
    """Weighted average cost of capital: E/V x Ke + D/V x Kd x (1 - t)."""
    if not 0 <= w.debt_weight < 1:
        raise ValuationError(f"debt weight must be in [0, 1), got {w.debt_weight}")
    ke = cost_of_equity(w.risk_free, w.beta, w.equity_risk_premium)
    kd_after_tax = w.pre_tax_cost_of_debt * (1 - w.tax_rate)
    value = (1 - w.debt_weight) * ke + w.debt_weight * kd_after_tax
    return {"cost_of_equity": ke, "after_tax_cost_of_debt": kd_after_tax,
            "equity_weight": 1 - w.debt_weight, "debt_weight": w.debt_weight, "wacc": value}


@dataclass
class DcfInputs:
    base_sales: float                 # last actual year (ex-disposals), USD m
    base_margin: float                # operating margin before exceptionals in the base year
    growth: list[float]               # organic sales growth per forecast year
    cumulative_savings: list[float]   # cumulative savings run-rate reached in each year, USD m
    flow_through: float               # share of savings that reaches operating profit
    tax_rate: float
    da_pct_sales: float
    capex_pct_sales: float
    nwc_pct_sales: float              # net working capital as % of sales (held constant)
    wacc: float
    terminal_growth: float
    years: list[int] = field(default_factory=list)
    stub_years: float = 0.0           # fraction of the first forecast year already elapsed at the valuation date
    mid_year: bool = False
    terminal_capex_pct_sales: float | None = None  # capex in the terminal year; None = same as the forecast years


def project(inp: DcfInputs) -> list[dict]:
    """Build the forecast: sales, EBIT, NOPAT and unlevered free cash flow per year.

    EBIT = sales x base margin + cumulative savings x flow-through
    (constant-margin base plus the share of the savings that is kept as profit).
    UFCF = NOPAT + D&A - capex - increase in net working capital.
    """
    n = len(inp.growth)
    if len(inp.cumulative_savings) != n:
        raise ValuationError("growth and savings schedules must have the same length")
    years = inp.years or list(range(1, n + 1))
    rows, prev_sales = [], inp.base_sales
    for i in range(n):
        sales = prev_sales * (1 + inp.growth[i])
        savings_kept = inp.cumulative_savings[i] * inp.flow_through
        ebit = sales * inp.base_margin + savings_kept
        nopat = ebit * (1 - inp.tax_rate)
        da = sales * inp.da_pct_sales
        capex = sales * inp.capex_pct_sales
        delta_nwc = (sales - prev_sales) * inp.nwc_pct_sales
        ufcf = nopat + da - capex - delta_nwc
        rows.append({"year": years[i], "sales": sales, "growth": inp.growth[i],
                     "savings_kept": savings_kept, "ebit": ebit, "ebit_margin": ebit / sales,
                     "ebitda": ebit + da, "tax": ebit * inp.tax_rate, "nopat": nopat, "da": da,
                     "capex": capex, "delta_nwc": delta_nwc, "ufcf": ufcf})
        prev_sales = sales
    return rows


def discount_periods(n: int, stub_years: float, mid_year: bool) -> list[float]:
    """Years from the valuation date to each cash flow.

    The first forecast year is only partly ahead of us (1 - stub). End-of-year convention by
    default; mid-year convention puts each cash flow in the middle of its (remaining) period.
    """
    if not 0 <= stub_years < 1:
        raise ValuationError("stub_years must be in [0, 1)")
    periods = []
    for i in range(n):
        end = (i + 1) - stub_years
        if mid_year:
            start = 0.0 if i == 0 else i - stub_years
            periods.append((start + end) / 2)
        else:
            periods.append(end)
    return periods


def terminal_year(inp: DcfInputs, last: dict) -> dict:
    """The first year after the forecast, built as a steady state growing at the terminal growth rate.

    Normalised terminal year (steady state): NOPAT, D&A and capex grow with sales at g, and the
    increase in working capital is only what g needs (sales x g x NWC %), not the faster growth
    of the last forecast year. Capex can be set separately for the steady state.
    """
    g = inp.terminal_growth
    capex_pct = inp.capex_pct_sales if inp.terminal_capex_pct_sales is None else inp.terminal_capex_pct_sales
    sales = last["sales"] * (1 + g)
    nopat = last["nopat"] * (1 + g)
    da = sales * inp.da_pct_sales
    capex = sales * capex_pct
    delta_nwc = (sales - last["sales"]) * inp.nwc_pct_sales
    ufcf = nopat + da - capex - delta_nwc
    # Reinvestment rate = (net capex + increase in NWC) / NOPAT; return on new invested capital = g / reinvestment rate
    reinvestment = capex - da + delta_nwc
    rate = reinvestment / nopat
    return {"sales": sales, "nopat": nopat, "da": da, "capex": capex, "capex_pct_sales": capex_pct,
            "delta_nwc": delta_nwc, "ufcf": ufcf, "reinvestment": reinvestment, "reinvestment_rate": rate,
            "implied_ronic": g / rate if rate > 0 else None}


def capex_pct_for_ronic(inp: DcfInputs, ronic: float) -> float:
    """Terminal capex (% of sales) that makes new investment earn a chosen return (RONIC).

    Value driver formula (McKinsey): reinvestment = g / RONIC x NOPAT. Reinvestment is net capex
    (capex - D&A) plus the increase in working capital, so capex = reinvestment - increase in NWC + D&A.
    """
    if ronic <= 0:
        raise ValuationError("RONIC must be positive")
    last = project(inp)[-1]
    probe = terminal_year(inp, last)
    reinvestment = inp.terminal_growth / ronic * probe["nopat"]
    return (reinvestment - probe["delta_nwc"] + probe["da"]) / probe["sales"]


def value(inp: DcfInputs) -> dict:
    """Enterprise value = PV of forecast UFCF + PV of terminal value (Gordon growth)."""
    if inp.terminal_growth >= inp.wacc:
        raise ValuationError(f"terminal growth {inp.terminal_growth:.2%} must be below WACC {inp.wacc:.2%}")
    rows = project(inp)
    periods = discount_periods(len(rows), inp.stub_years, inp.mid_year)
    pv_total = 0.0
    for i, (r, t) in enumerate(zip(rows, periods)):
        cf = r["ufcf"] * ((1 - inp.stub_years) if i == 0 else 1.0)  # only the unelapsed part of year 1
        df = 1 / (1 + inp.wacc) ** t
        r.update({"cash_flow_counted": cf, "period": t, "discount_factor": df, "pv": cf * df})
        pv_total += cf * df
    last = rows[-1]
    term = terminal_year(inp, last)
    # Gordon growth terminal value at the end of the last forecast year: next year's normalised FCF / (WACC - g)
    tv = term["ufcf"] / (inp.wacc - inp.terminal_growth)
    # Terminal value sits at the end of the final year and assumes next year's cash arrives a year later.
    # Under the mid-year convention every later year's cash also arrives mid-year, so the whole perpetuity
    # is half a year nearer: discount it over (N - stub - 0.5) years, consistent with the forecast years.
    tv_period = len(rows) - inp.stub_years - (0.5 if inp.mid_year else 0.0)
    pv_tv = tv / (1 + inp.wacc) ** tv_period
    ev = pv_total + pv_tv
    return {"rows": rows, "terminal_year": term, "pv_forecast": pv_total, "terminal_value": tv, "pv_terminal_value": pv_tv,
            "enterprise_value": ev, "tv_share_of_ev": pv_tv / ev,
            "implied_exit_ev_ebitda": tv / last["ebitda"]}


@dataclass
class Bridge:
    net_debt: float
    lease_liabilities: float = 0.0      # only if not already inside net debt
    minority_interests: float = 0.0
    pension_deficit: float = 0.0
    associates: float = 0.0             # added: their profits are not in operating profit
    disposal_proceeds: float = 0.0      # added if not yet reflected in net debt
    restructuring_cash: float = 0.0     # announced one-off cash costs not in the forecast or net debt: debt-like
    contingent_liabilities: float = 0.0 # claims the PM assumes will be paid (e.g. a tax case assumed lost): debt-like
    # Proportionate minorities: if set, minorities = this share x EV (outside shareholders' share of the operating
    # profit the DCF values), replacing the book value in minority_interests.
    minority_share_of_ev: float | None = None


def minorities_deducted(enterprise_value: float, b: Bridge) -> float:
    """Value of minority interests (non-controlling interests) to deduct from EV.

    Proportionate method: the DCF values consolidated cash flows (100% of each subsidiary), so the outside
    shareholders' slice is valued the same way: their share of operating profit x enterprise value.
    Otherwise the reported (book) value is used.
    """
    if b.minority_share_of_ev is None:
        return b.minority_interests
    if not 0 <= b.minority_share_of_ev < 1:
        raise ValuationError("minority share of EV must be between 0 and 1")
    return b.minority_share_of_ev * enterprise_value


def roll_forward(equity_value: float, cost_of_equity: float, years: float, dividends: float = 0.0) -> float:
    """Equity value at the balance sheet date carried forward to the valuation date.

    Shareholders expect to earn the cost of equity, so value grows at Ke until the valuation date,
    less any dividend that went ex in between (that cash belongs to the previous holders).
    """
    if years < 0:
        raise ValuationError("roll-forward period must not be negative")
    return equity_value * (1 + cost_of_equity) ** years - dividends


def equity_bridge(enterprise_value: float, b: Bridge, shares_m: float, fx_usd_per_gbp: float | None,
                  roll: dict | None = None) -> dict:
    """EV -> equity value -> value per share in USD and, for a London price, pence (GBp).

    Equity = EV - net debt - leases - minorities (see minorities_deducted) - pension deficit - restructuring cash
             - contingent liabilities + associates + disposal proceeds.
    If `roll` is given ({cost_of_equity, years, dividends}), EV and the bridge are at the balance sheet date
    and the equity value is rolled forward to the valuation date (see roll_forward).
    Per share (GBp) = equity (USD) / shares / (USD per GBP) x 100. With no FX rate (a US-dollar share price),
    only the USD figure is produced.
    """
    if shares_m <= 0 or (fx_usd_per_gbp is not None and fx_usd_per_gbp <= 0):
        raise ValuationError("shares and FX rate must be positive")
    minorities = minorities_deducted(enterprise_value, b)
    equity_bs = (enterprise_value - b.net_debt - b.lease_liabilities - minorities - b.pension_deficit
                 - b.restructuring_cash - b.contingent_liabilities + b.associates + b.disposal_proceeds)
    equity = equity_bs if roll is None else roll_forward(equity_bs, roll["cost_of_equity"], roll["years"],
                                                         roll.get("dividends", 0.0))
    per_share_usd = equity / shares_m
    per_share_gbp = None if fx_usd_per_gbp is None else per_share_usd / fx_usd_per_gbp
    return {"enterprise_value": enterprise_value, "minorities_deducted": minorities,
            "equity_value_balance_sheet_date": equity_bs, "equity_value": equity,
            "per_share_usd": per_share_usd, "per_share_gbp": per_share_gbp,
            "per_share_gbp_pence": None if per_share_gbp is None else per_share_gbp * 100}


def sensitivity(inp: DcfInputs, wacc_values: list[float], growth_values: list[float],
                terminal_ronic: float | None = None) -> list[list[float | None]]:
    """Enterprise value for each (WACC, terminal growth) pair. None where growth >= WACC.

    If terminal capex is set by a return on new investment (RONIC), it is re-derived for each cell,
    because the reinvestment needed for growth g is g / RONIC x NOPAT.
    """
    grid = []
    for w in wacc_values:
        row = []
        for g in growth_values:
            if g >= w:
                row.append(None)
                continue
            trial = DcfInputs(**{**inp.__dict__, "wacc": w, "terminal_growth": g})
            if terminal_ronic is not None:
                trial.terminal_capex_pct_sales = capex_pct_for_ronic(trial, terminal_ronic)
            row.append(value(trial)["enterprise_value"])
        grid.append(row)
    return grid
