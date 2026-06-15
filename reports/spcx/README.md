# SPCX morning reports

Dated archive of the morning SPCX (SpaceX) technical/flow updates produced by
[`/spcx-morning`](../../.claude/commands/spcx-morning.md), scheduled by
[`.github/workflows/spcx-morning.yml`](../../.github/workflows/spcx-morning.yml).

- One file per market day: `YYYY-MM-DD.md`
- Cron: 12:00 UTC, Mon–Fri (≈ 08:00 ET in EDT; 07:00 ET in EST)
- Mode is adaptive — quick changelog by default, full re-analysis on lockup /
  earnings / index inclusion / >5% overnight move days
- Trigger a one-off run from the Actions tab via *Run workflow*; the
  `force_mode` input lets you pick `quick` / `full` / `auto`

Each report is **not investment advice** — see disclaimer at the bottom of
every file.
