"""Value SPCX using management's OWN forward guidance from the Q2 2026
earnings call (Aug 4, 2026 — SpaceX's first as a public company).

Guidance taken from the call (speakers: Musk; Gwynne Shotwell, President;
Bret Johnsen, CFO):
  G1. "$100 billion in annualized recurring revenue by the end of the year"
      (Johnsen) — largest contribution from AI cloud agreements incl. the
      closed Google deal (~$920M/month) and Anthropic, ramping in Q4.
      NOTE: on ~2 GW of end-2026 compute this can only be CONTRACTED
      bookings, not delivered revenue; modeled as revenue arriving 2027-28
      as capacity comes online.
  G2. "Our internal projections for reaching $1 trillion in revenue have
      moved up from 2031 to 2030, and there's a non-zero chance of that
      being in 2029." (Musk)
  G3. Capex "for the next two quarters will be similar to Q2's $18.4B"
      (Johnsen) -> FY2026 capex ~$63-65B; AI compute capex has "less than
      a one-year payback ... almost like a COGS item" -> implies AI
      sales-to-capital >= ~1.0, which this model adopts (1.1 early, 1.5 late).
  G4. Compute: 1.4 GW today -> 2 GW end-2026 -> ~10 GW end-2027 (15 GW
      aspiration, 20 GW stretch).
  G5. Starlink: 12.0M subs (+17% QoQ, 2x YoY), ARPU $66/mo (down from $85
      YoY — price-for-volume); standalone Starlink Mobile sats fly 2027.
  G6. Starship: daily-launch cadence "probably a year from now"; human
      rating by end-2027; crewed Moon 2028 (Shotwell); uncrewed Mars +
      Optimus this Nov-Dec window. Adjacent optionality, not revenue here.
  G7. Q2 adjusted EBITDA $3.5B (+191%), 45% margin; GAAP net loss $541M.

Framework: same ginzu mechanics as damodaran_blog_update.py (his tax ramp,
cost of capital 8.37% -> 8.25%, terminal g = riskfree 4.56%), with explicit
revenue paths instead of target-interpolation. Balance sheet: cash $93.5B,
book debt $22.9B, 13,159M shares.

Scenarios:
  1. Face value  — guidance lands as spoken: $1T in 2030, ~$2.0T by 2036.
  2. Musk-time   — everything 3 years late ($1T in 2033), the historical
                   slippage pattern (Model 3 ramp, FSD, robotaxi).
  3. Half-right  — signed AI contracts are real but growth normalizes
                   after 2028; revenue plateaus toward $550B.
Weighted 15/35/40 plus 10% on a $20 bear (execution/funding break).

Usage: python musk_guidance_dcf.py          ($B throughout)
"""

TAXES = [0.10, 0.10, 0.10, 0.10, 0.10, 0.13, 0.16, 0.19, 0.22, 0.25]
RF = 0.0456
COC0, COC_T = 0.0837, 0.0825
CASH, DEBT, SHARES = 93.5, 22.9, 13.159
PRICE = 111.0
BEAR_VPS, W = 20.0, (0.15, 0.35, 0.40, 0.10)


def coc(t):
    return COC0 if t < 5 else COC0 + (COC_T - COC0) * (t - 4) / 5


def dcf(name, base_rev, revs, m0, mT, conv_yr, s2c0, s2c1, roic_T):
    pv, disc, prev = 0.0, 1.0, base_rev
    for t in range(10):
        m = m0 + (mT - m0) * min((t + 1) / conv_yr, 1.0)
        ebit = revs[t] * m
        s2c = s2c0 + (s2c1 - s2c0) * t / 9
        reinv = max(revs[t] - prev, 0.0) / s2c
        fcff = ebit * (1 - TAXES[t]) - reinv
        disc *= 1 + coc(t)
        pv += fcff / disc
        prev = revs[t]
    ebit_term = revs[-1] * mT * (1 + RF)
    fcff_term = ebit_term * (1 - TAXES[-1]) * (1 - RF / roic_T)
    tv = fcff_term / (COC_T - RF)
    equity = pv + tv / disc + CASH - DEBT
    vps = equity / SHARES
    print(f"{name:12s} 2030 rev {revs[3]:>5,.0f} | 2036 rev {revs[-1]:>5,.0f} "
          f"@ {mT:.0%} | equity ${equity/1000:,.2f}T | ${vps:>7,.2f}/share "
          f"({vps/PRICE-1:+.0%} vs ${PRICE:.0f})")
    return vps


if __name__ == "__main__":
    print("Scenario        2030rev      2036rev        equity        value/share\n" + "-" * 76)
    face = dcf("Face value", 35,
               [110, 280, 550, 1000, 1250, 1475, 1670, 1820, 1940, 2030],
               m0=-0.06, mT=0.35, conv_yr=7, s2c0=1.1, s2c1=1.5, roic_T=0.18)
    late = dcf("3 yrs late", 33,
               [60, 110, 200, 330, 500, 700, 870, 1000, 1090, 1140],
               m0=-0.06, mT=0.32, conv_yr=9, s2c0=1.0, s2c1=1.4, roic_T=0.15)
    half = dcf("Half right", 33,
               [90, 160, 230, 300, 360, 420, 470, 510, 535, 550],
               m0=-0.06, mT=0.30, conv_yr=8, s2c0=1.0, s2c1=1.4, roic_T=0.15)
    ev = W[0] * face + W[1] * late + W[2] * half + W[3] * BEAR_VPS
    print("-" * 76)
    print(f"Guidance-weighted (15% face / 35% late / 40% half / 10% bear $20): "
          f"${ev:,.2f}/share ({ev/PRICE-1:+.0%} vs market ${PRICE:.0f})")
