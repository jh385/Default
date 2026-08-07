"""Aswath Damodaran's ACTUAL SpaceX valuation (his fcff-ginzu workbook,
'SpaceX2026IPOUpdated.xlsx', valuation date 2026-06-01 — the model behind his
June 'Post-Prospectus Update' post), ported faithfully to Python, then re-run
with the Q2 2026 information set.

Every mechanic below was lifted from the workbook itself (Input sheet /
Valuation output / Stories to Numbers), stored in the repo at
models/SpaceX2026IPOUpdated.xlsx:

  - Four segments with 2036 revenue targets: Launch $40B, Starlink $120B,
    xAI $160B, Other $100B (total $420B in year 10).
  - Segment revenue paths: base + (target - base) * phi_t, with his workbook's
    phi schedule (front-loaded: 1/15 of the gap in year 1, 1/3 by year 5);
    'Other' ramps 0 -> 100B in $20B steps over years 6-10.
  - Segment operating margins converge linearly to targets by year 10:
    Launch 8% -> 45%, Starlink 10% -> 60%, xAI -5% -> 25%, Other 0% -> 30%
    (base margins are post-R&D-capitalization allocations).
  - Tax: 10% effective years 1-5, stepping to the 25% marginal by year 10.
  - Reinvestment: delta-revenue / sales-to-capital, by segment:
    Launch 3 (yrs 1-5) / 4 (6-10); Starlink 3/5; xAI 1.5/2.5; Other 5/5.
  - Cost of capital 8.37% years 1-5, linear to 8.25% by year 10 (his
    override); terminal growth = riskfree 4.56%; terminal ROIC 15%.
  - Equity bridge: operating assets - book debt ($22,896M) + cash ($24,747M)
    + $75,000M IPO proceeds; shares 12,535.3M + shares issued at INTRINSIC
    value for the proceeds (the workbook's circular/iterative step).
  - His outputs (reproduced by this port to the cent): operating assets
    $1,224,448M; equity $1,301,299M; 13,301.95M shares; $97.83/share
    vs the $135 offer ("price at 138% of value").

Q2 2026 actuals used for the update (Aug 4 release / CNBC): revenue $7.81B
(+92%: Connectivity $4.29B +66%, AI $2.6B +247%, launch ~$0.92B flat);
capex $18.37B in the quarter ($15.83B AI); cash $93.5B; shares 13.159B
post-greenshoe; price ~$111.

Usage: python damodaran_blog_update.py     ($M throughout)
"""

PHI = [0.066667, 0.146667, 0.221333, 0.277333, 0.333333,
       0.466667, 0.626667, 0.776000, 0.888000, 1.000000]
PHI_OTHER = [0, 0, 0, 0, 0, 0.2, 0.4, 0.6, 0.8, 1.0]
TAX = [0.10, 0.10, 0.10, 0.10, 0.10, 0.13, 0.16, 0.19, 0.22, 0.25]
RF = 0.0456
COC0, COC_T = 0.0837, 0.0825
ROIC_T = 0.15


def coc(t):                        # years 1-5 initial, linear to terminal by yr 10
    return COC0 if t < 5 else COC0 + (COC_T - COC0) * (t - 4) / 5


def margin_path(m0, mT):
    return [m0 + (mT - m0) * (t + 1) / 10 for t in range(10)]


def value(segs, cash, debt, shares, ipo_proceeds=0.0, label="", verbose=True):
    """segs: dict name -> (base_rev, target_rev, m0, mT, s2c_1to5, s2c_6to10, phi)."""
    revs = {k: [b + (T - b) * phi[t] for t in range(10)]
            for k, (b, T, m0, mT, s1, s2, phi) in segs.items()}
    margins = {k: margin_path(v[2], v[3]) for k, v in segs.items()}

    pv, disc = 0.0, 1.0
    y1_reinv = None
    for t in range(10):
        ebit = sum(revs[k][t] * margins[k][t] for k in segs)
        reinv = 0.0
        for k, (b, T, m0, mT, s1, s2, phi) in segs.items():
            prev = revs[k][t - 1] if t else b
            reinv += max(revs[k][t] - prev, 0.0) / (s1 if t < 5 else s2)
        if t == 0:
            y1_reinv = reinv
        fcff = ebit * (1 - TAX[t]) - reinv
        disc *= 1 + coc(t)
        pv += fcff / disc

    ebit10 = sum(segs[k][1] * segs[k][3] for k in segs)      # targets hit in yr 10
    ebit_term = ebit10 * (1 + RF)
    fcff_term = ebit_term * (1 - TAX[-1]) * (1 - RF / ROIC_T)
    tv = fcff_term / (COC_T - RF)
    op_assets = pv + tv / disc

    equity = op_assets - debt + cash + ipo_proceeds
    if ipo_proceeds:                     # his circular step: new shares at intrinsic value
        vps = equity / shares
        for _ in range(50):
            vps = equity / (shares + ipo_proceeds / vps)
        n_shares = shares + ipo_proceeds / vps
    else:
        vps, n_shares = equity / shares, shares

    if verbose:
        rev10 = sum(segs[k][1] for k in segs)
        print(f"{label}")
        print(f"  Yr-10 revenue ${rev10/1000:,.0f}B, EBIT ${ebit10/1000:,.0f}B "
              f"({ebit10/rev10:.1%}) | yr-1 reinvestment ${y1_reinv/1000:,.1f}B")
        print(f"  Op assets ${op_assets/1000:,.0f}B | equity ${equity/1000:,.0f}B "
              f"| {n_shares/1000:,.2f}B sh -> ${vps:,.2f}/share\n")
    return vps


# --- 1. His June model exactly as in the workbook -------------------------
HIS = {
    "Launch":   (4086, 40000, 0.08, 0.45, 3, 4, PHI),
    "Starlink": (11387, 120000, 0.10, 0.60, 3, 5, PHI),
    "xAI":      (3201, 160000, -0.05, 0.25, 1.5, 2.5, PHI),
    "Other":    (0, 100000, 0.00, 0.30, 5, 5, PHI_OTHER),
}

# --- 2. Q2-updated: only inputs the Aug 2026 information set contradicts --
#   Bases re-anchored to TTM-Jun-2026 (Launch flat, Starlink +66%, xAI +247%);
#   Launch 2036 target trimmed 40 -> 30B (flat YoY tape vs his 26%/yr path);
#   xAI sales-to-capital cut 1.5/2.5 -> 0.6/1.5 and Starlink 3/5 -> 2/4
#   (Q2: $18.4B capex vs ~$3.7B revenue growth in the quarter — his yr-1
#   reinvestment of ~$10B/yr is running ~5x below actual);
#   balance sheet actuals: cash $93.5B (IPO done, so no proceeds/share
#   circularity), shares 13,159M, book debt held at $22,896M.
Q2 = {
    "Launch":   (4000, 30000, 0.08, 0.45, 2, 3, PHI),
    "Starlink": (14100, 120000, 0.10, 0.60, 2, 4, PHI),
    "xAI":      (6550, 160000, -0.05, 0.25, 0.6, 1.5, PHI),
    "Other":    (0, 100000, 0.00, 0.30, 5, 5, PHI_OTHER),
}

if __name__ == "__main__":
    value(HIS, cash=24747, debt=22896, shares=12535.3, ipo_proceeds=75000,
          label="1. Damodaran June 2026 (port of his workbook; his output: $97.83)")
    value(Q2, cash=93500, debt=22896, shares=13159,
          label="2. Q2-updated (his framework, August 2026 information set)")

    q2_his_s2c = {k: (v[0], v[1], v[2], v[3], HIS[k][4], HIS[k][5], v[6])
                  for k, v in Q2.items()}
    value(q2_his_s2c, cash=93500, debt=22896, shares=13159,
          label="3. Q2 bases but HIS sales-to-capital (isolates the capex shock)")

    upside = dict(Q2)
    upside["Starlink"] = (14100, 150000, 0.10, 0.60, 2, 4, PHI)
    upside["xAI"] = (6550, 200000, -0.05, 0.25, 0.6, 1.5, PHI)
    value(upside, cash=93500, debt=22896, shares=13159,
          label="4. Q2-updated upside (Starlink $150B, xAI $200B on Q2 momentum)")
