---
description: Adaptive morning SPCX (SpaceX) technical/flow analysis — quick changelog by default, full re-analysis on key event days.
allowed-tools: WebSearch, WebFetch, Read, Write, Bash(date:*), Bash(git log:*), Bash(ls:*), Bash(cat reports/spcx/*)
---

# /spcx-morning — adaptive morning SPCX analysis

Produce a morning technical/flow update for SPCX (SpaceX, NASDAQ — IPO'd 2026-06-12).
Two modes, selected automatically.

## Step 1 — Determine today's mode

Today is $(date +"%Y-%m-%d").

**Check the escalation triggers** (use WebSearch + the dated tables below).
Escalate to FULL mode if ANY of these is true today:

- Today is a **scheduled lockup-tranche date** (see schedule below)
- Today is a **scheduled or rumored earnings date** for SpaceX
- Today is the effective date of an **index inclusion** (Russell 1000: 2026-06-26 close; MSCI USA: ~2026-06-25; Nasdaq-100: ~early July 2026)
- Today is a **Mars launch window day** (Nov–Dec 2026)
- **Overnight move > 5%** in either direction
- A **Form 144 / 4 filing** by a SpaceX insider was published since yesterday's run
- A major **Starship test flight** is scheduled today
- The **last successful run was >3 calendar days ago** (catch up from a gap)

Otherwise → QUICK mode.

### Lockup tranche calendar (escalate on any of these)

| Date | Tranche |
|---|---|
| ~2026-08-11 (or 2 days post-Q2 earnings — confirm date) | 20% (+10% conditional if SPCX ≥ $175.50 on 5 of 10 days into earnings) |
| 2026-08-21 (day 70) | 7% |
| 2026-09-10 (day 90) | 7% |
| 2026-09-25 (day 105) | 7% |
| 2026-10-10 (day 120) | 7% |
| 2026-10-25 (day 135) | 7% |
| Q3 earnings date (late Oct / early Nov) | 28% |
| 2026-12-08 (day 180) | Remainder (non-Musk) |
| 2027-06-12 (day 366) | Musk + select investors |

### Catalyst calendar (escalate on day-of)

- 2026-06-25 → MSCI USA inclusion effective (~10 trading days post-IPO)
- 2026-06-26 (after close) → Russell 1000 / Top 200 inclusion effective
- Early July 2026 → Nasdaq-100 inclusion (15 trading days post-listing)
- Options listing day (TBA late June 2026)
- ~2026-09-02 → first public Q2 earnings (per StockAlarm; may shift earlier to ~Aug 11)
- Nov–Dec 2026 → Mars transfer window (uncrewed Starship Mars attempt)
- Late 2026 / early 2027 → NASA HLS uncrewed lunar flyby

## Step 2 — Gather the data

Use WebSearch for the freshest data. Always pull:

1. **Last close + premarket**: search `SPCX stock price premarket` and `SPCX close` for today's date.
   Compute % move vs. yesterday's close. (Also check `SPCX 52-week high low` for new ATHs.)
2. **Overnight news**: search `SPCX news` and `SpaceX news` for the last 24h.
3. **Filings**: search `site:sec.gov SPCX OR "Space Exploration"` for any new filings since yesterday's run.
4. **Flows**: search `SPCX ARK holdings`, `SPCX 13F`, `SPCX short interest` — note any newly-reported numbers.
5. **Index status check**: only relevant near inclusion dates; otherwise skip.

If the file `reports/spcx/<yesterday>.md` exists, **read it first** so you can frame today
as a delta. (Use `ls reports/spcx/` to find the most recent prior report — it may not be
literally yesterday if the cron skipped a weekend / holiday.)

Cross-check at least 2 sources for any price you cite. If a number conflicts across
sources, report a range and flag the conflict.

## Step 3 — Write the report

Write the output to `reports/spcx/<today YYYY-MM-DD>.md` using the structure below.
Today's date is $(date +"%Y-%m-%d").

### QUICK mode (default — ~300–500 words)

```markdown
# SPCX — Morning Update <YYYY-MM-DD>

**Mode:** Quick changelog · **Prior run:** <date of last report or "n/a">

## Tape
- Last close: $X.XX (DoD ±X.XX%)
- Premarket: $X.XX (±X.XX%)
- Day 1 anchor: $135 IPO · $160.95 day-1 close
- Key levels: support $X / $X · resistance $X / $X

## What moved
- <1–3 bullets — biggest overnight news / filings / flows>

## Lockup countdown
- Next tranche: <date> (<N> days), <%> of insider block (~XM shares)
- Days to Dec 8 cliff: <N>

## Index status
- Russell 1000: <IN / pending — 6/26> · MSCI USA: <IN / pending — 6/25> · Nasdaq-100: <IN / pending — early Jul> · S&P 500: blocked (seasoning + profitability)

## Flow / positioning watch
- <ARK net buy/sell since prior run; any 13F snippets; short interest if reported>

## What to watch today
- <1–3 specific items: levels, scheduled events, filings to monitor>

## Confidence
- <low / medium / high> · note any data conflicts

---
Sources:
- <linked URLs, one per bullet that needs one>
```

### FULL mode (escalation — ~1500–2500 words)

Re-run a condensed version of the 5-angle deep-research pipeline:
1. Identification check (has SPCX been re-tickered, split, etc.?)
2. Supply/demand metrics (float, ownership, ARK, 13F if any, short interest)
3. Lockup status (next tranche, recent Form 144s, bonus-trigger status)
4. Index inclusion (active or pending effective dates, passive flow estimates)
5. Technicals (price action, MAs once meaningful, RSI/MACD if reliable, support/resistance, options if listed)

For each angle, pull from at least 2 distinct sources and cite URLs.
Include a **Year-end 2026 price scenario table** (bull/base/bear ranges with prob weights)
if today is a major event day or the prior run is >7 days stale.

End the report with:
- "## What changed vs. <prior report date>" — a bullet list of deltas
- "## Sources" — every URL cited, deduped

## Step 4 — Save & commit

- Write to `reports/spcx/<YYYY-MM-DD>.md`.
- If running interactively, also print a 4-line summary to chat (date, mode, current price, biggest delta).
- The GitHub Action wrapper handles the `git add / commit / push`. Do NOT push manually here.

## Hard rules

- This is **not investment advice**. Always include a one-line disclaimer at the bottom.
- Never invent numbers. If a metric is missing, write "n/a" and explain why in 1 line.
- Year/month consistency: if you see a date from before today, sanity-check it isn't a stale article being misread.
- If WebSearch returns nothing for a query, try a reworded query before giving up.
- Keep links inline as markdown `[label](url)` — the GitHub Action will surface them.
