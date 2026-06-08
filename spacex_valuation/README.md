# SpaceX Daily Valuation

A small, dependency-free tool that produces a **daily estimated valuation of
SpaceX** and emails it as a digest.

SpaceX is privately held — there is no live market price. So this is an honest
*model*, not a quote: it anchors to reported funding rounds, employee/investor
tender offers, and secondary share sales, then estimates any given day's value
by **log-linear (constant-growth) interpolation** between the two surrounding
anchor points. The anchors live in [`data/funding_rounds.json`](data/funding_rounds.json),
each with a source link.

> **Disclaimer:** This is a modeled estimate built from public reporting. It is
> not a quoted price, an offer, or investment advice. Figures are approximate.

## What it produces

```
SpaceX Daily Valuation — Jun 8, 2026: ~$1.720T
==============================================

Estimated valuation: ~$1.720T  (1,719,987,870,906 USD)
Day-over-day change: +0.4334%
Method: log-linear interpolation between anchors (upper anchor is a projected IPO target)
...
```

The email digest ships as both plain text and a styled HTML version.

## Usage

No third-party packages — just Python 3.9+.

```bash
cd spacex_valuation

python valuation.py                      # today's digest (plain text)
python valuation.py --date 2026-06-08    # a specific day
python valuation.py --format html        # HTML digest
python valuation.py --date 2024-09-01 --json   # machine-readable estimate
```

### Sending the email

`send_digest.py` is stdlib-only (`smtplib`). Configure via environment variables:

| Variable      | Meaning                                            |
|---------------|----------------------------------------------------|
| `SMTP_HOST`   | e.g. `smtp.gmail.com`                              |
| `SMTP_PORT`   | `587` (STARTTLS) or `465` (SSL)                   |
| `SMTP_USER`   | SMTP login                                          |
| `SMTP_PASS`   | password / app password                            |
| `DIGEST_FROM` | From: address (defaults to `SMTP_USER`)            |
| `DIGEST_TO`   | comma-separated recipients                          |
| `SMTP_SSL`    | `1` for implicit SSL (port 465)                    |

```bash
python send_digest.py --dry-run          # preview, don't send
python send_digest.py                     # send today's digest
```

**Gmail:** create an [App Password](https://myaccount.google.com/apppasswords)
(Google Account → Security → App passwords) and use it as `SMTP_PASS` with
`SMTP_HOST=smtp.gmail.com`, `SMTP_PORT=587`, `SMTP_USER=you@gmail.com`.

## Running it daily

### Option A — GitHub Actions (recommended)

[`.github/workflows/daily-valuation.yml`](../.github/workflows/daily-valuation.yml)
runs every day at 13:00 UTC. Add the variables above as repository secrets
(Settings → Secrets and variables → Actions). Trigger a manual test run from the
Actions tab via "Run workflow" (supports a `dry_run` input).

### Option B — cron

```cron
# 9am daily
0 9 * * *  cd /path/to/spacex_valuation && \
  SMTP_HOST=smtp.gmail.com SMTP_PORT=587 SMTP_USER=you@gmail.com \
  SMTP_PASS=app_password DIGEST_TO=you@gmail.com \
  /usr/bin/python3 send_digest.py >> /tmp/spacex_digest.log 2>&1
```

## Keeping the model current

When a new funding round, tender, or secondary sale is reported, add an anchor
to [`data/funding_rounds.json`](data/funding_rounds.json) with its date,
valuation, per-share price (if known), and a `source` URL. The daily estimate
updates automatically. Anchors flagged `"projected": true` (e.g. the expected
IPO target) are used as the *upper* bound for interpolation but the value is
held flat once that date passes.

## How the estimate is computed

For a target date `t` between anchors `(d0, v0)` and `(d1, v1)`:

```
v(t) = v0 * (v1 / v0) ** ((t - d0) / (d1 - d0))
```

i.e. constant geometric growth between known points. Before the first anchor or
after the last *completed* anchor, the value is held flat. Day-over-day change
is `v(t) / v(t-1) - 1`.
