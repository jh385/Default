# SPCX — Damodaran-Style Intrinsic Valuation

**Prepared:** 2026-08-07 · **Price:** ~$111 (Aug 6 finish; vendor prints $111–114, Aug 5 close $108.27) · **Model:** [`spacex_valuation/damodaran_dcf.py`](../../spacex_valuation/damodaran_dcf.py)
**Framework:** Aswath Damodaran's young-growth FCFF template — story → revenue decay → margin convergence → reinvestment via sales-to-capital → evolving cost of capital → terminal value. First intrinsic (cash-flow-anchored) valuation in this series; everything prior was comps and analogies.

## TL;DR

| Scenario | 2036 revenue | Equity value | **$/share** | vs ~$111 |
|---|---|---|---|---|
| Bear — Starlink plateaus, AI burns capital at cost of capital | $120B | $110B | **$8** | −92% |
| **Base — executes well, not miraculously** | $225B | $339B | **$26** | −77% |
| Bull — street-high (Goldman-ish) path, AWS-class margins | $319B | $655B | **$50** | −55% |
| Musk — $1T revenue by 2031, 32% margins | $1,690B | $4,165B | **$316** | +185% |
| **Scenario-weighted (25/45/25/5)** | — | — | **~$42** | **−62%** |

**Reverse DCF:** today's ~$111 requires ~148% year-1 growth decaying to 4%, i.e. **2030 revenue ~$368B** (right between Morgan Stanley's $330B and Goldman's $474B street-high forecasts) **and 2036 revenue ~$780B at 28% mature margins with 15% terminal ROIC.** The market is not pricing the base case; it is pricing the street's most aggressive published path, roughly 60% of the way to Musk's own claims.

**Cross-check against Damodaran's actual model (§6):** his own June workbook values SPCX at **$97.83/share** ($1.30T equity); re-run with the Q2 actuals it yields **~$91** (range $91–106 across variants). The stock at ~$111, which IPO'd 38% above his value, now trades within ~10–20% of Damodaran-fair. The gap between his ~$91 and this report's $42 is almost entirely his terminal margin structure (38% blended vs 24% here).

## 1. The story (Damodaran step one: what kind of company is this?)

SpaceX is three businesses wearing one ticker, per its own S-1 segments (FY2025: $18.7B revenue, recast to include xAI/X):

1. **Connectivity/Starlink — the cash engine.** $11.4B in 2025 (61% of revenue), Q2 2026 $4.29B (+66% YoY), 12.0M subscribers (2x YoY), the only consistently profitable segment (2025 op income $4.4B, EBITDA ~$7.2B). Economics: subscription telecom with a depreciating orbital capital stock — mature analog is a global ISP/telco, ~20–25% operating margins.
2. **Space/launch — the moat, not the money.** ~$4.1B in 2025, near-monopoly heavy-lift. Mature analog: aerospace/defense, ~12–15% margins, moderate growth.
3. **AI (xAI) — the capital furnace.** $3.2B in 2025, Q2 2026 $2.6B (+247% YoY) — and $15.8B of the quarter's $18.4B capex. Economics today: hyperscaler build-out with none of a hyperscaler's margins yet. This segment is why FY2025 showed a $4.9B net loss and why cash ($93.5B post-IPO) matters.

The valuation question Damodaran would pose: *when this company is mature, what does it earn on what it has invested?* The answer drives everything below.

## 2. Inputs and why

| Lever | Base case | Rationale |
|---|---|---|
| Base-year revenue (FY2026E) | $31B | H1 2026 actual $13.2B (Q1 $5.4B + Q2 $7.81B, +92% YoY); H2 ramp continues. Company claims $100B *run-rate* exiting 2026 — treated as bull/Musk material, not base |
| Year-1 revenue growth | 65%, decaying geometrically to 4% by 2036 | Below the company's claim, above simple deceleration; 2030 lands at $128B (street-high notes say $330–474B — those live in Bull) |
| Mature operating margin | 24% by 2033 (from ~−10% FY2026E) | Blend: Starlink telco ~22%, launch ~13%, AI infra ~28% if it works; 2025 op margin was −14%, Q2 2026 ~−7% and improving |
| Sales-to-capital | 0.7 → 1.3 | The punishing lever. Q2 2026 actual: $18.4B capex vs ~$3.7B revenue *growth* — currently far below 0.7; assumes discipline arrives with scale |
| Tax | 23% after a ~$10B NOL burns off | US statutory + state, standard Damodaran treatment |
| Cost of capital | 10.4% → 8.0% by 2036 | Bottom-up: Rf 4.2%, ERP ~4.8%, levered beta ~1.4 (telecom 0.8 / semis-AI 1.6 / aero 1.3 blend), minimal debt; mature converges toward market average |
| Terminal | g = 4% (= Rf), ROIC 12% → reinvest 33% of after-tax EBIT | Modest excess return (ROIC − WACC ≈ 4pts) for moat durability; terminal EV/EBIT ≈ 13x — a sanity-passing mature multiple |
| Balance sheet | +$93.5B cash (Q2 actual) − $15B debt (**assumption**, xAI data-center financing; not verified from filings) | Net cash ~$78B ≈ $6/share of the value in every scenario |
| Shares | 13.159B (post-greenshoe) | No separate dilution haircut: future raises at fair value are NPV-neutral in the FCFF framework; below-fair-value raises are a real risk the framework can't price |

Scenario deltas: Bear = 35% y1 growth, 16% margin, S2C 0.6→1.0, terminal ROIC 8% (= WACC — growth adds nothing); Bull = 85% y1, 28% margin by 2032, S2C 0.9→1.5, ROIC 15%; Musk = explicit path hitting $1T in 2031 (his own target, pulled forward at Q2 earnings), 32% margins, ROIC 20%.

## 3. Base case, year by year ($B)

| Yr | Revenue | Margin | EBIT | Reinvest | FCFF | WACC | PV |
|---|---|---|---|---|---|---|---|
| 2027 | 51.1 | −5.1% | −2.6 | 28.8 | **−31.4** | 10.4% | −28.5 |
| 2028 | 75.5 | −0.3% | −0.2 | 31.8 | **−32.0** | 10.1% | −26.3 |
| 2029 | 102.0 | 4.6% | 4.7 | 31.7 | −27.0 | 9.9% | −20.2 |
| 2030 | 128.1 | 9.4% | 12.1 | 29.1 | −17.9 | 9.6% | −12.2 |
| 2031 | 152.3 | 14.3% | 21.8 | 25.0 | −8.2 | 9.3% | −5.1 |
| 2032 | 173.3 | 19.1% | 33.2 | 20.3 | +5.2 | 9.1% | +3.0 |
| 2033 | 190.8 | 24.0% | 45.8 | 16.0 | +19.3 | 8.8% | +10.2 |
| 2034 | 205.0 | 24.0% | 49.2 | 12.2 | +25.7 | 8.5% | +12.5 |
| 2035 | 216.2 | 24.0% | 51.9 | 9.1 | +30.9 | 8.3% | +13.8 |
| 2036 | 224.8 | 24.0% | 54.0 | 6.7 | +34.9 | 8.0% | +14.5 |

Terminal value $720B (PV $299B) + interim FCFF PV −$38B → **EV $260B** + net cash $78B → **equity $339B → $25.75/share**. Note the shape: five straight years of negative free cash flow (financed by the IPO war chest — $93.5B covers the cumulative ~$116B nominal burn only with more raising, which is why the S2C discipline assumption matters more than the growth assumption).

## 4. Value vs. price — the Damodaran distinction

The gap between $42 (weighted intrinsic) and $111 (price) is not a math error; it is the difference between the *value* process (cash flows, discounted) and the *price* process (flows, mood, momentum): a 4.9%→11.8% float, forced index buying (Russell, MSCI, Nasdaq-100 at ~1.3%), a staggered-lockup supply calendar, and the Musk narrative premium. Two honest caveats cut opposite ways:

- **This framework has been "wrong" for years at a time.** Damodaran's own DCFs valued Tesla far below market through most of 2013–2020 and prompted him to exit Nvidia at a fraction of its later peak. When a story company *delivers* its story, intrinsic value migrates up to meet price — each earnings print re-writes the inputs.
- **What would move the value:** evidence the AI segment earns above its cost of capital (today it is 82% of capex and ~14% of revenue); Starlink margin expansion at scale (the +79% YoY segment-income growth in Q2 is genuinely value-positive); capex discipline (any quarter where sales-to-capital beats ~0.7); and the $100B run-rate claim actually materializing by year-end (that alone would push the base toward the bull).

**Watch-items that re-rate this model:** Q3 earnings (~Nov), first Form 144 flows from the Aug 6 unlock, Dec 8 lockup cliff, the end-2026 run-rate vs. the $100B claim, and any standalone disclosure of xAI's debt (the $15B assumption here is the softest input).

## 5. Reconciling with the 2036 Tesla-track ladder

The DCF reframes the ladder rather than replacing it. If intrinsic value today is ~$26–50 (base–bull) and value compounds at the cost of equity once fairly priced, the *DCF-fair* 2036 price is roughly **$60–115** — below even the stage-matched ~$150, and orders of magnitude below the literal track. Conversely, the earlier scale-honest band ($750–1,350) implicitly assumes SpaceX *delivers something between the Bull and Musk cash-flow paths and keeps a premium multiple*. In DCF language: the 2036 ladder is a menu of price outcomes; this model says which of them come with cash flows attached.

| Mark | $/share | 1,900 shares |
|---|---|---|
| Intrinsic, bear | $8 | $16K |
| Intrinsic, base | $26 | $49K |
| **Intrinsic, scenario-weighted** | **$42** | **$80K** |
| Intrinsic, bull | $50 | $95K |
| Market price (Aug 6) | ~$111 | ~$211K |
| Intrinsic, Musk case | $316 | $601K |

Read plainly: at ~$111 the market currently pays ~2.6x the weighted intrinsic value of the position — which is either a gift (if you believe the model) or a discount (if you believe Musk's revenue path). The honest statement is that **$111 is only cheap in the one scenario where the company's own forecasts come true.**

## 6. Damodaran's actual valuation — checked against Q2 (added 2026-08-07)

Damodaran has published two SPCX pieces on Musings on Markets: ["To a Trillion(s) Dollars and beyond: A SpaceX IPO Odyssey!"](https://aswathdamodaran.blogspot.com/2026/04/to-trillion-dollars-and-beyond-spacex.html) (April) and ["Revisiting the SpaceX Valuation: A Post-Prospectus Update!"](https://aswathdamodaran.blogspot.com/2026/06/a-weeks-ago-i-assessed-value-of-spacex.html) (June, also [on Substack](https://aswathdamodaran.substack.com/p/revisiting-the-spacex-valuation-a)). This section works from **his actual June valuation workbook** (`SpaceX2026IPOUpdated.xlsx`, valuation date 2026-06-01, archived in this repo at [`spacex_valuation/models/`](../../spacex_valuation/models/)), ported line-for-line to [`damodaran_blog_update.py`](../../spacex_valuation/damodaran_blog_update.py) — the port reproduces his published output to within $0.03/share.

**His actual June model:** four segments with 2036 revenue targets — **Launch $40B / Starlink $120B / xAI $160B / "Other" $100B** (the Other segment is a pure optionality bet that ramps $0 → $100B in years 6–10) — total **$420B year-10 revenue at a 38.1% blended operating margin** (targets: Launch 45%, Starlink 60%, xAI 25%, Other 30%, converging linearly by year 10 from post-R&D-capitalization base margins). Sales-to-capital: Launch 3→4, Starlink 3→5, xAI 1.5→2.5, Other 5. Tax 10% effective stepping to 25% marginal; cost of capital 8.37%→8.25%; terminal growth = riskfree 4.56%; terminal ROIC 15% (override). Bridge: operating assets **$1,224B** − book debt $22.9B + cash $24.7B + $75B IPO proceeds (with new shares issued at *intrinsic* value — his workbook's iterative step) → equity **$1,301B** on 13,302M shares = **$97.83/share** vs the $135 offer ("price at 138% of value"). His story caveats: the S-1's $26T AI TAM is "reaching the end of what's plausible"; the gap to the IPO price is "one isolated bet on xAI compute"; his number is "a relative, disciplined estimate, not a price target."

**The Q2 check** — where the Aug 4 print confirms or breaks his actual inputs:

| His June assumption | Q2 2026 actual | Verdict → revision |
|---|---|---|
| Year-1 (2026) revenue $38.8B (Launch $6.5B / Starlink $18.6B / xAI $13.7B) | Run-rate ~$31B (Launch ~$3.8B, Starlink ~$17.2B, xAI ~$10.4B annualized) | **Behind his path** overall — though Q2 beat the street, and the company's $100B exit-run-rate claim would leapfrog it. Bases re-anchored to TTM |
| Launch to $40B by 2036 (~26%/yr) | ~$0.92B in Q2, roughly **flat** YoY | Behind → target trimmed to $30B |
| Starlink to $120B, 60% margin | +66% revenue, segment income +79%, subs 2x | On/ahead of track → held (his $120B needs only 24%/yr from the TTM base) |
| xAI to $160B, 25% margin | $2.6B, **+247%** YoY | Ramp ahead → base raised; **target held** (his TAM skepticism concerns the endpoint, not the slope) |
| Year-1 reinvestment **$10.2B** (S2C: xAI 1.5, Starlink 3) | **$18.4B capex in Q2 alone** ($15.8B AI) — actual reinvestment ~5x his path | The big break → xAI S2C cut 1.5/2.5 → 0.6/1.5, Starlink 3/5 → 2/4 |
| Year-1 EBIT +$3.3B (margin ramp) | GAAP op loss narrowing (net −$541M) but still negative | Slightly behind; margin *schedules* held (his base margins are R&D-adjusted; 2025 adj. EBITDA was +$6.6B) |
| Cash $24.7B + $75B proceeds; 13,302M shares (issued at intrinsic $97.83) | Cash $93.5B actual; 13,159M shares — the deal priced at $135, **above** his intrinsic value | Actuals swapped in; selling stock above intrinsic value was accretive (fewer shares than he modeled) |

**Result: the Q2-updated value in his own framework is $91.23/share (equity ~$1.20T), −6.7% vs his June $97.83.** Decomposition: the capex/sales-to-capital shock alone is worth **−$4.86** (running Q2 bases with *his* original S2C gives $96.09); the launch trim and balance-sheet actuals account for the rest; Starlink's faster base partially offsets. Upside variant (Starlink $150B, xAI $200B on Q2 momentum, capex cut retained): **$106.06**. So his framework post-Q2 brackets **$91–106** — the stock at ~$111, which IPO'd 38% *above* Damodaran-fair, has round-tripped to within ~5–20% of it. On his stated discipline (buy below value), SPCX first became arguable at the Aug 5 low of $105–108.

**Why his ~$91 vs this report's $42 weighted:** the margin lever, full stop. His terminal structure — $420B revenue at 38.1% blended operating margin, with year-10 ROIC of **64%** on his sales-to-capital assumptions — prices SpaceX's mature state like scaled software infrastructure; this report's base (24% margin, 12% terminal ROIC) prices it like an excellent industrial. His June year-1 reinvestment of $10.2B against Q2's actual $18.4B *per quarter* is the live test of which world we're in: if capex normalizes toward his path by 2028, his number wins; if $60–70B/yr persists, even $91 is generous. In the §2 scenario grid, his inputs sit squarely between Bull and Musk.

| Mark | $/share | 1,900 shares |
|---|---|---|
| This report, weighted intrinsic | $42 | $80K |
| **Damodaran, Q2-updated (his workbook, his levers)** | **$91** | **$173K** |
| Damodaran June (his workbook output) | $97.83 | $186K |
| Damodaran Q2 upside variant | $106 | $202K |
| Market (Aug 6) | ~$111 | ~$211K |

## Sources

Model inputs from previously verified data (see [2036-tesla-track.md](2036-tesla-track.md)) plus: [CNBC — Q2 2026 earnings](https://www.cnbc.com/2026/08/04/spacex-spcx-earnings-live-updates-q2-2026.html) · [Yahoo — S-1 financials](https://finance.yahoo.com/markets/stocks/articles/6-charts-spacex-1-financials-225255139.html) · [Motley Fool — Aug 6 unlock](https://www.fool.com/investing/2026/08/05/spacexs-lockup-expires-on-aug-6-heres-why-9115-mil/) · [TradingKey — Aug 6 close](https://www.tradingkey.com/news/market-movers/262084964-market-movers-spcx-20260806). Framework: A. Damodaran, *The Dark Side of Valuation* / "Valuing Young, Start-up and Growth Companies."

---

**Not investment advice.** A DCF is a disciplined way to be precisely uncertain: every number above is an assumption wearing a suit. The $15B debt figure and ~$10B NOL are explicit guesses; segment-level ROIC is not yet disclosed; the framework assigns no probability of distress (net cash makes it remote) and no value to real options (Mars, spectrum, compute resale) that a Musk bull would argue are the whole point.
