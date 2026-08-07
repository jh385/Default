"""Damodaran-style FCFF valuation of SpaceX (Nasdaq: SPCX).

Framework (per Aswath Damodaran's young-growth-company template):
  1. Revenue: year-1 growth rate decaying geometrically to the terminal
     (risk-free) rate by year 10 — or an explicit revenue path.
  2. Operating margin: converges from today's (negative) margin to a
     target mature margin by a convergence year.
  3. Reinvestment: delta-revenue / sales-to-capital ratio (ramping as the
     satellite + AI-datacenter build-out matures).
  4. Taxes: 23% on positive EBIT after a net-operating-loss carryforward
     is exhausted.
  5. Cost of capital: starts at a young-growth rate, declines linearly to
     a mature rate by year 10.
  6. Terminal value: FCFF_11 / (wacc_mature - g), with terminal
     reinvestment = g / terminal ROIC.
  7. Equity = PV(FCFF) + PV(TV) + cash - debt; per share on 13.159B shares.

Base-year inputs (FY2026E, as of 2026-08-06):
  H1 2026 actual revenue $13.2B (Q1 $5.4B + Q2 $7.81B, +92% YoY);
  FY2026E ~$31B. Cash $93.5B (post-IPO, Q2 10-Q). Debt ~$15B (assumed,
  xAI data-center financing; S-1 recast — flagged, not verified).
  NOL ~$10B (2025 loss $4.9B + prior). Shares 13.159B. Price ~$111.

Usage: python damodaran_dcf.py
"""

YEARS = 10
BASE_REV = 31.0          # $B, FY2026E
CASH = 93.5              # $B
DEBT = 15.0              # $B (assumption — see docstring)
NOL0 = 10.0              # $B carryforward
SHARES = 13.159          # B shares
PRICE = 111.0            # ~Aug 6 2026
TAX = 0.23
RF = 0.042               # 10-yr UST assumption
G_TERM = 0.04            # terminal growth ~ risk-free
WACC_MATURE = 0.08

MARGIN0 = -0.10          # FY2026E operating margin (2025: -14%; improving)


def growth_path(g1, g_last=G_TERM, n=YEARS):
    """Geometric decay from g1 (year 1) to g_last (year n)."""
    return [g1 * (g_last / g1) ** (t / (n - 1)) for t in range(n)]


def lerp(a, b, t, n):
    return a + (b - a) * min(t / (n - 1), 1.0)


def dcf(name, g1=None, rev_path=None, margin_target=0.24, margin_year=8,
        s2c_start=0.7, s2c_end=1.3, roic_term=0.12, wacc_start=0.104,
        verbose=False):
    """Returns dict with value per share and diagnostics."""
    if rev_path is None:
        g = growth_path(g1)
        revs, r = [], BASE_REV
        for gt in g:
            r *= 1 + gt
            revs.append(r)
    else:
        revs = list(rev_path)
        assert len(revs) == YEARS

    nol = NOL0
    pv_sum = 0.0
    disc = 1.0
    rows = []
    prev_rev = BASE_REV
    for t in range(YEARS):
        rev = revs[t]
        # margin converges linearly to target by margin_year
        margin = lerp(MARGIN0, margin_target, t + 1, margin_year)
        margin = min(margin, margin_target)
        ebit = rev * margin
        # taxes with NOL shield
        if ebit > 0:
            shield = min(nol, ebit)
            nol -= shield
            tax = TAX * (ebit - shield)
        else:
            nol += -ebit
            tax = 0.0
        s2c = lerp(s2c_start, s2c_end, t, YEARS)
        reinvest = max(rev - prev_rev, 0.0) / s2c
        fcff = ebit - tax - reinvest
        wacc = lerp(wacc_start, WACC_MATURE, t, YEARS)
        disc *= 1 + wacc
        pv_sum += fcff / disc
        rows.append((2027 + t, rev, margin, ebit, reinvest, fcff, wacc, fcff / disc))
        prev_rev = rev

    # terminal value off year-10 EBIT
    ebit_t = revs[-1] * min(lerp(MARGIN0, margin_target, YEARS, margin_year), margin_target)
    at_ebit = ebit_t * (1 - TAX)
    reinvest_ratio = G_TERM / roic_term
    fcff11 = at_ebit * (1 + G_TERM) * (1 - reinvest_ratio)
    tv = fcff11 / (WACC_MATURE - G_TERM)
    pv_tv = tv / disc

    ev = pv_sum + pv_tv
    equity = ev + CASH - DEBT
    vps = equity / SHARES

    if verbose:
        print(f"\n  {'yr':4s} {'rev':>7s} {'margin':>7s} {'EBIT':>7s} {'reinv':>7s} {'FCFF':>8s} {'WACC':>6s} {'PV':>8s}")
        for r in rows:
            print(f"  {r[0]:4d} {r[1]:7.1f} {r[2]:7.1%} {r[3]:7.1f} {r[4]:7.1f} {r[5]:8.1f} {r[6]:6.2%} {r[7]:8.1f}")
        print(f"  TV: EBIT_10 {ebit_t:.1f} -> FCFF_11 {fcff11:.1f} -> TV {tv:,.0f} (PV {pv_tv:,.0f})")

    return {"name": name, "rev36": revs[-1], "ev": ev, "equity": equity,
            "vps": vps, "pv_fcff": pv_sum, "pv_tv": pv_tv}


def solve_reverse(target_vps, **kw):
    """Solve year-1 growth so DCF value equals target (bull-style settings)."""
    lo, hi = 0.05, 3.0
    for _ in range(80):
        mid = (lo + hi) / 2
        v = dcf("solve", g1=mid, **kw)["vps"]
        if v < target_vps:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


if __name__ == "__main__":
    scenarios = [
        dict(name="Bear  — Starlink plateaus, AI burns", g1=0.35,
             margin_target=0.16, margin_year=8, s2c_start=0.6, s2c_end=1.0,
             roic_term=0.08, wacc_start=0.11),
        dict(name="Base  — executes well, not miraculously", g1=0.65,
             margin_target=0.24, margin_year=8, s2c_start=0.7, s2c_end=1.3,
             roic_term=0.12, wacc_start=0.104),
        dict(name="Bull  — street-high (Goldman-ish) path", g1=0.85,
             margin_target=0.28, margin_year=7, s2c_start=0.9, s2c_end=1.5,
             roic_term=0.15, wacc_start=0.10),
        dict(name="Musk  — $1T revenue by 2031", rev_path=[90, 220, 450, 750, 1000, 1200, 1380, 1520, 1625, 1690],
             margin_target=0.32, margin_year=6, s2c_start=1.1, s2c_end=1.8,
             roic_term=0.20, wacc_start=0.10),
    ]
    weights = [0.25, 0.45, 0.25, 0.05]

    print(f"{'Scenario':44s} {'2036 rev':>9s} {'EV':>8s} {'Equity':>8s} {'$/share':>8s} {'vs $111':>8s}")
    results = []
    for sc in scenarios:
        r = dcf(**sc)
        results.append(r)
        print(f"{r['name']:44s} {r['rev36']:8.0f}B {r['ev']:7.0f}B {r['equity']:7.0f}B "
              f"{r['vps']:8.2f} {r['vps']/PRICE-1:+8.1%}")

    wv = sum(w * r["vps"] for w, r in zip(weights, results))
    print(f"\nScenario-weighted (25/45/25/5): ${wv:,.2f}/share "
          f"({wv/PRICE-1:+.1%} vs market ${PRICE:.0f})")

    g_star = solve_reverse(PRICE, margin_target=0.28, margin_year=7,
                           s2c_start=0.9, s2c_end=1.5, roic_term=0.15, wacc_start=0.10)
    r_star = dcf("implied", g1=g_star, margin_target=0.28, margin_year=7,
                 s2c_start=0.9, s2c_end=1.5, roic_term=0.15, wacc_start=0.10)
    print(f"\nReverse DCF: ${PRICE:.0f} implies year-1 growth ~{g_star:.0%} "
          f"(decaying to 4%), i.e. 2036 revenue ~${r_star['rev36']:,.0f}B "
          f"at 28% mature margins")

    print("\nDetail (Base case):")
    dcf(**{**scenarios[1], "verbose": True})
