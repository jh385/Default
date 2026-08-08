# SPCX — Valuing the Stock on Management's Own Guidance

**Prepared:** 2026-08-07 · **Price:** ~$111 · **Model:** [`spacex_valuation/musk_guidance_dcf.py`](../../spacex_valuation/musk_guidance_dcf.py)
**Source:** SpaceX's first-ever earnings call (Q2 2026, Aug 4) — Musk, President Gwynne Shotwell, CFO Bret Johnsen — plus the Q2 release. This model deliberately uses **management's numbers, not the street's and not Damodaran's**, then prices the credibility question explicitly.

## TL;DR

| Scenario | 2030 revenue | 2036 revenue | Equity | **$/share** | vs $111 |
|---|---|---|---|---|---|
| **Face value** — guidance lands as spoken ($1T in 2030) | $1,000B | $2,030B | $5.69T | **$432** | +289% |
| **Three years late** — the historical Musk slippage pattern | $330B | $1,140B | $2.53T | **$192** | +73% |
| **Half right** — signed AI deals real, growth normalizes post-2028 | $300B | $550B | $1.21T | **$92** | −17% |
| **Guidance-weighted** (15/35/40 + 10% bear at $20) | — | — | — | **~$171** | **+54%** |

Two independent cross-checks land on top of earlier work: "half right" ($92) is within a dollar of the Q2-updated Damodaran value ($91), and "three years late" ($192) sits almost exactly at the street's $210 consensus target — the sell-side is implicitly pricing *"Musk, but late."*

## 1. The guidance ledger (what was actually said on the call)

| # | Guidance | Speaker | Model treatment |
|---|---|---|---|
| G1 | **"$100 billion in annualized recurring revenue by the end of the year"** — largest contribution from AI cloud agreements, incl. the closed **Google deal (~$920M/month)** and Anthropic, ramping in Q4 | Johnsen | See the bookings caveat below — modeled as contracted revenue *delivered* 2027–28 as capacity builds |
| G2 | **"Our internal projections for reaching $1 trillion in revenue have moved up from 2031 to 2030, and there's a non-zero chance of that being in 2029"** | Musk | Face-value path hits $1T in 2030 (the 2029 option is ignored) |
| G3 | Capex "for the next two quarters will be similar to Q2's $18.4B"; AI compute has **"less than a one-year payback … almost like a COGS item"** | Johnsen | FY2026 capex ~$64B; the payback claim *is* a sales-to-capital assertion — adopted as S2C 1.1→1.5 |
| G4 | Compute: 1.4 GW live → 2 GW end-2026 → **~10 GW end-2027** (15 GW aim, 20 GW stretch) | Musk | Feasibility check on the revenue ramp (~$10–12B/GW-yr of AI revenue) |
| G5 | Starlink: **12.0M subs** (+17% QoQ, 2x YoY), **ARPU $66/mo, down from $85** a year ago; standalone Starlink Mobile satellites fly 2027 | Johnsen/Shotwell | Price-for-volume: supports subscriber growth, caps connectivity ARPU upside |
| G6 | Starship: daily launch cadence "probably a year from now"; human-rating end-2027; **crewed Moon 2028**; uncrewed Mars + Optimus robots this Nov–Dec window | Musk/Shotwell | Optionality, not revenue — deliberately excluded |
| G7 | Q2 adjusted EBITDA **$3.5B (+191% YoY, ~45% margin)**; GAAP net loss $541M | Johnsen | Anchors the margin-convergence path |

**The $100B "ARR" caveat — the most important analytical catch on the call:** on the ~2 GW of compute SpaceX will have at year-end, $100B of *delivered* annualized revenue is physically impossible (it would imply ~$40B/GW-yr; hyperscaler economics are ~$10–12B/GW-yr). The figure only works as **contracted bookings against future capacity** — Google's $920M/month plus Anthropic and others, revenue recognized through 2027–28 as the 10–15 GW build completes. The model therefore shows FY2027 revenue of ~$110B in the face-value case rather than an instant step to $100B+, and the first hard test of guidance is whether the Q4 report (Feb 2027) shows that contracted backlog.

## 2. Model construction

Same ginzu mechanics as the Damodaran port (his tax ramp 10%→25%, cost of capital 8.37%→8.25%, terminal growth = riskfree 4.56%), with explicit guidance-derived revenue paths; balance sheet actuals (cash $93.5B, book debt $22.9B, 13,159M shares). Face value: revenue $110B (2027) → $280B → $550B → **$1,000B (2030)**, then decaying growth to ~$2.03T by 2036 (≈1.7% of world GDP); operating margin −6% → 35% by 2033 (consistent with 45% adjusted-EBITDA prints under heavy D&A); S2C 1.1→1.5 *because the CFO claimed it*; terminal ROIC 18%. The slippage scenario shifts the same curve three years right (the Model-3-ramp pattern); the half-right scenario lets 2027–28 land near contract-supported levels then fade to GDP-plus growth.

**The funding hole the face-value path implies:** with revenue additions of $170–450B/yr against S2C ~1.2, mid-path reinvestment runs $150–350B/yr — FCFF stays deeply negative into the early 2030s (2030 alone: ~$210B NOPAT vs ~$350B reinvestment). Cumulatively that's roughly **$300–400B of external funding beyond the IPO war chest** — continuous raises or debt. The FCFF framework treats fair-value issuance as neutral; in practice this is the mechanism by which "face value" degrades into "three years late."

## 3. Read-through

- **Guidance-weighted value ~$171 (+54%)** — the only model in this series that puts intrinsic value meaningfully *above* the market price, and it requires believing management's own numbers at 15% face / 35% late / 40% half.
- **The triangulation is now tight:** Damodaran-updated $91 ≈ guidance-half-right $92 (independent constructions); street consensus $210 ≈ guidance-three-years-late $192; my conservative weighted $42 = the world where the AI capex never earns its payback claim. Today's $111 sits between "half right" and the weighted guidance value — the market is charging a partial-credibility premium, which is exactly where a rational price should sit.
- **The single decisive variable is the CFO's sub-one-year-payback claim.** If AI capex genuinely returns $1+/yr of revenue per dollar within a year, the Q2 "capex shock" was the market misreading a COGS-like item as empire-building, and value migrates toward $192–432. If payback stretches, the same spend is the bear case. Q3 (Nov) and Q4 (Feb 2027) AI-segment revenue against the ~$34B H1 AI capex will answer it quickly.
- **For 1,900 shares:** half-right $174K · weighted $324K · late $365K · face value $821K, vs ~$211K at market.

## Sources

[CNBC — Q2 2026 earnings live updates](https://www.cnbc.com/2026/08/04/spacex-spcx-earnings-live-updates-q2-2026.html) · [Seeking Alpha — SPCX Q2 2026 earnings call transcript](https://seekingalpha.com/article/4930329-space-exploration-technologies-corp-spcx-q2-2026-earnings-call-transcript) · [Fortune — "totally nuts" moon robots + $1T target](https://fortune.com/2026/08/04/elon-musk-spacex-earnings-trillion-revenue-target-capex-stock-reaction/) · [Yahoo — Musk on $1T possibly a year early](https://finance.yahoo.com/markets/stocks/articles/musk-says-spacex-revenue-could-225745291.html) · [TechCrunch — Anthropic & Google compute deals](https://techcrunch.com/2026/08/04/spacex-doubles-revenues-on-anthropic-and-google-compute-deals-starlink-growth/) · [Not a Tesla App — call highlights](https://www.notateslaapp.com/news/4543/highlights-from-spacexs-first-ever-earnings-call-starship-starlink-grok-and-more) · [Space.com — Starship cadence](https://www.space.com/space-exploration/launches-spacecraft/spacex-wants-to-launch-next-starship-this-month-and-catch-it-too-elon-musk-says-in-1st-earnings-call-since-historic-ipo) · [SEC — Q2 2026 8-K earnings release](https://www.sec.gov/Archives/edgar/data/0001181412/000162828026052515/earningsreleaseq22608042.htm)

---

**Not investment advice.** This model prices management's statements, which are aspirations with a documented slippage history, not commitments. Transcript quotes were compiled from press coverage of the call (several transcript hosts are blocked from this environment); the guidance ledger marks each claim's speaker.
