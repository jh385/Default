"""SpaceX daily valuation model.

SpaceX is privately held, so there is no live market price. This module
estimates a daily valuation by anchoring to reported funding rounds, tender
offers, and secondary share sales (see data/funding_rounds.json) and
interpolating between the two surrounding anchor points on a log-linear
(constant-growth) basis.

The estimate is exactly that — an estimate. Between two anchors the implied
growth rate is held constant; before the first anchor or after the last
non-projected anchor the value is held flat.

Usage:
    python valuation.py                 # today's digest (plain text)
    python valuation.py --date 2026-06-08
    python valuation.py --format html   # HTML digest
    python valuation.py --json          # machine-readable estimate
"""

from __future__ import annotations

import argparse
import json
import math
import os
from datetime import date, datetime, timedelta
from typing import Optional

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "funding_rounds.json")
HOLDINGS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "holdings.json")


def load_data(path: str = DATA_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_holdings(path: str = HOLDINGS_PATH) -> Optional[dict]:
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _parse(d: str) -> date:
    return datetime.strptime(d, "%Y-%m-%d").date()


def estimate_valuation(target: date, data: dict) -> dict:
    """Estimate SpaceX's valuation on ``target`` from the anchor points.

    Returns a dict describing the estimate, the bounding anchors, the method
    used, and the implied annualized growth between those anchors.
    """
    anchors = sorted(data["anchors"], key=lambda a: a["date"])
    points = [(_parse(a["date"]), float(a["valuation_usd"]), a) for a in anchors]

    first_d, first_v, first_a = points[0]
    last_d, last_v, last_a = points[-1]

    if target <= first_d:
        return {
            "date": target.isoformat(),
            "valuation_usd": first_v,
            "method": "held flat at earliest anchor",
            "lower_anchor": first_a,
            "upper_anchor": None,
            "annualized_growth": None,
        }

    if target >= last_d:
        # Hold flat at the last *actual* (non-projected) anchor.
        for d, v, a in reversed(points):
            if not a.get("projected") and d <= target:
                return {
                    "date": target.isoformat(),
                    "valuation_usd": v,
                    "method": "held flat at latest completed anchor",
                    "lower_anchor": a,
                    "upper_anchor": None,
                    "annualized_growth": None,
                }
        return {
            "date": target.isoformat(),
            "valuation_usd": last_v,
            "method": "held flat at latest anchor",
            "lower_anchor": last_a,
            "upper_anchor": None,
            "annualized_growth": None,
        }

    # Between two anchors: log-linear (constant geometric growth) interpolation.
    for (d0, v0, a0), (d1, v1, a1) in zip(points, points[1:]):
        if d0 <= target <= d1:
            span = (d1 - d0).days
            frac = (target - d0).days / span if span else 0.0
            value = v0 * (v1 / v0) ** frac
            annualized = (v1 / v0) ** (365.0 / span) - 1.0 if span else None
            return {
                "date": target.isoformat(),
                "valuation_usd": value,
                "method": "log-linear interpolation between anchors"
                + (" (upper anchor is a projected IPO target)" if a1.get("projected") else ""),
                "lower_anchor": a0,
                "upper_anchor": a1,
                "annualized_growth": annualized,
            }

    raise RuntimeError("interpolation failed — anchors not covering target date")


def daily_change(target: date, data: dict) -> Optional[float]:
    """Fractional change in the estimate from the previous day, or None."""
    today_v = estimate_valuation(target, data)["valuation_usd"]
    prev_v = estimate_valuation(target - timedelta(days=1), data)["valuation_usd"]
    if prev_v == 0:
        return None
    return (today_v - prev_v) / prev_v


def latest_firm_mark(target: date, data: dict) -> Optional[dict]:
    """Most recent anchor on/before ``target`` that has an actual (non-projected)
    reported per-share price — the best market-set per-share mark available."""
    candidates = [
        a for a in data["anchors"]
        if a.get("per_share") and not a.get("projected") and _parse(a["date"]) <= target
    ]
    return max(candidates, key=lambda a: a["date"]) if candidates else None


def per_share_estimate(target: date, data: dict) -> Optional[float]:
    """Model per-share value: interpolated total valuation / implied shares
    outstanding. ``None`` if shares outstanding is unknown."""
    shares = data.get("shares_outstanding_estimate")
    if not shares:
        return None
    total = estimate_valuation(target, data)["valuation_usd"]
    return total / shares


def position(shares: float, target: date, data: dict) -> dict:
    """Mark a holding of ``shares`` to the current best estimates.

    Returns both a firm mark (latest reported market per-share price) and the
    model mark (interpolated total / implied shares outstanding)."""
    firm = latest_firm_mark(target, data)
    firm_ps = float(firm["per_share"]) if firm else None
    model_ps = per_share_estimate(target, data)
    return {
        "shares": shares,
        "firm_per_share": firm_ps,
        "firm_source": firm,
        "firm_value": shares * firm_ps if firm_ps is not None else None,
        "model_per_share": model_ps,
        "model_value": shares * model_ps if model_ps is not None else None,
    }


def fmt_usd(value: float) -> str:
    """Human-friendly large-dollar formatting ($1.75T, $350.0B, $122M)."""
    abs_v = abs(value)
    if abs_v >= 1e12:
        return f"${value / 1e12:.3f}T"
    if abs_v >= 1e9:
        return f"${value / 1e9:.1f}B"
    if abs_v >= 1e6:
        return f"${value / 1e6:.1f}M"
    return f"${value:,.0f}"


def _pct(frac: Optional[float]) -> str:
    if frac is None:
        return "n/a"
    return f"{frac * 100:+.4f}%"


def build_digest(target: date, data: dict, shares: Optional[float] = None) -> dict:
    est = estimate_valuation(target, data)
    change = daily_change(target, data)
    anchors = sorted(data["anchors"], key=lambda a: a["date"])

    # Recent anchor history (last 6) for context.
    recent = anchors[-6:]

    pos = position(shares, target, data) if shares else None

    subject = f"SpaceX Daily Valuation — {target.strftime('%b %-d, %Y')}: ~{fmt_usd(est['valuation_usd'])}"
    if pos and pos["firm_value"] is not None:
        subject += f" | your {shares:g} sh ≈ {fmt_usd(pos['firm_value'])}"
    return {
        "subject": subject,
        "estimate": est,
        "daily_change": change,
        "recent_anchors": recent,
        "events": data.get("events", []),
        "target": target,
        "position": pos,
    }


def render_text(digest: dict) -> str:
    est = digest["estimate"]
    lines = []
    lines.append(digest["subject"])
    lines.append("=" * len(digest["subject"]))
    lines.append("")
    lines.append(f"Estimated valuation: ~{fmt_usd(est['valuation_usd'])}  ({est['valuation_usd']:,.0f} USD)")
    lines.append(f"Day-over-day change: {_pct(digest['daily_change'])}")
    lines.append(f"Method: {est['method']}")
    if est.get("annualized_growth") is not None:
        lines.append(f"Implied annualized growth between anchors: {est['annualized_growth'] * 100:.1f}%")
    lines.append("")

    pos = digest.get("position")
    if pos:
        lines.append(f"YOUR POSITION — {pos['shares']:g} shares")
        if pos["firm_value"] is not None:
            src = pos["firm_source"]
            lines.append(
                f"  Firm mark:  {pos['shares']:g} × ${pos['firm_per_share']:,.2f}/sh = {fmt_usd(pos['firm_value'])}"
                f"  ({pos['firm_value']:,.0f} USD)"
            )
            lines.append(f"              based on {src['label']} ({src['date']})")
        if pos["model_value"] is not None:
            lines.append(
                f"  Model mark: {pos['shares']:g} × ${pos['model_per_share']:,.2f}/sh = {fmt_usd(pos['model_value'])}"
                f"  ({pos['model_value']:,.0f} USD)"
            )
            lines.append("              interpolated total valuation / implied shares outstanding")
        lines.append("")

    lo, hi = est.get("lower_anchor"), est.get("upper_anchor")
    lines.append("Bracketing anchors:")
    if lo:
        lines.append(f"  • {lo['date']}  {lo['label']:<38} {fmt_usd(float(lo['valuation_usd']))}")
    if hi:
        lines.append(f"  • {hi['date']}  {hi['label']:<38} {fmt_usd(float(hi['valuation_usd']))}")
    lines.append("")

    lines.append("Recent anchor history:")
    for a in digest["recent_anchors"]:
        ps = f"  (~${a['per_share']:.0f}/sh)" if a.get("per_share") else ""
        proj = "  [projected]" if a.get("projected") else ""
        lines.append(f"  {a['date']}  {fmt_usd(float(a['valuation_usd'])):>9}  {a['label']}{ps}{proj}")
    lines.append("")

    if digest["events"]:
        lines.append("Recent corporate events:")
        for e in digest["events"]:
            lines.append(f"  {e['date']}  {e['label']}")
        lines.append("")

    lines.append("-" * 68)
    lines.append(
        "DISCLAIMER: SpaceX is privately held. This is a modeled ESTIMATE built\n"
        "by interpolating between reported funding rounds and tender offers — not\n"
        "a quoted price, an offer, or investment advice. Figures are approximate."
    )
    return "\n".join(lines)


def render_html(digest: dict) -> str:
    est = digest["estimate"]
    change = digest["daily_change"]
    change_color = "#16a34a" if (change or 0) >= 0 else "#dc2626"

    rows = []
    for a in digest["recent_anchors"]:
        ps = f"~${a['per_share']:.0f}" if a.get("per_share") else "—"
        proj = ' <span style="color:#9ca3af">(projected)</span>' if a.get("projected") else ""
        rows.append(
            f"<tr><td style='padding:6px 12px;border-bottom:1px solid #eee'>{a['date']}</td>"
            f"<td style='padding:6px 12px;border-bottom:1px solid #eee;text-align:right;font-weight:600'>{fmt_usd(float(a['valuation_usd']))}</td>"
            f"<td style='padding:6px 12px;border-bottom:1px solid #eee;text-align:right'>{ps}</td>"
            f"<td style='padding:6px 12px;border-bottom:1px solid #eee'>{a['label']}{proj}</td></tr>"
        )
    rows_html = "\n".join(rows)

    ann = ""
    if est.get("annualized_growth") is not None:
        ann = f"<p style='margin:4px 0;color:#555'>Implied annualized growth between anchors: <b>{est['annualized_growth']*100:.1f}%</b></p>"

    pos = digest.get("position")
    pos_html = ""
    if pos and pos["firm_value"] is not None:
        src = pos["firm_source"]
        model_line = ""
        if pos["model_value"] is not None:
            model_line = (
                f"<div style='margin-top:6px;color:#c3cad6;font-size:13px'>Model mark "
                f"(interpolated): {pos['shares']:g} × ${pos['model_per_share']:,.2f} = "
                f"<b style='color:#fff'>{fmt_usd(pos['model_value'])}</b></div>"
            )
        pos_html = f"""
    <div style="background:#10243a;color:#fff;padding:18px 28px;border-top:1px solid #1f3a59">
      <div style="font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#7fa8d4">Your position — {pos['shares']:g} shares</div>
      <div style="font-size:30px;font-weight:800;margin-top:6px;line-height:1">{fmt_usd(pos['firm_value'])}</div>
      <div style="margin-top:4px;color:#c3cad6;font-size:13px">Firm mark: {pos['shares']:g} × ${pos['firm_per_share']:,.2f}/sh &nbsp;·&nbsp; {src['label']} ({src['date']})</div>
      {model_line}
    </div>"""

    return f"""<!DOCTYPE html>
<html><body style="margin:0;background:#f3f4f6;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#111">
  <div style="max-width:640px;margin:0 auto;padding:24px">
    <div style="background:#0b0f19;color:#fff;border-radius:14px 14px 0 0;padding:24px 28px">
      <div style="font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:#8b95a7">SpaceX Daily Valuation</div>
      <div style="font-size:15px;color:#c3cad6;margin-top:4px">{digest['target'].strftime('%A, %B %-d, %Y')}</div>
      <div style="font-size:46px;font-weight:800;margin-top:14px;line-height:1">~{fmt_usd(est['valuation_usd'])}</div>
      <div style="margin-top:8px;font-size:16px;color:{change_color};font-weight:700">{_pct(change)} <span style="color:#8b95a7;font-weight:400">day over day</span></div>
    </div>{pos_html}
    <div style="background:#fff;border-radius:0 0 14px 14px;padding:20px 28px;box-shadow:0 1px 3px rgba(0,0,0,.08)">
      <p style="margin:4px 0;color:#555">Method: <b>{est['method']}</b></p>
      {ann}
      <h3 style="margin:22px 0 8px;font-size:15px">Recent anchor points</h3>
      <table style="border-collapse:collapse;width:100%;font-size:14px">
        <thead><tr style="text-align:left;color:#6b7280">
          <th style="padding:6px 12px">Date</th>
          <th style="padding:6px 12px;text-align:right">Valuation</th>
          <th style="padding:6px 12px;text-align:right">Per&nbsp;share</th>
          <th style="padding:6px 12px">Event</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
      <p style="margin:22px 0 0;font-size:12px;color:#9ca3af;line-height:1.5">
        SpaceX is privately held. This is a modeled <b>estimate</b> built by interpolating
        between reported funding rounds and tender offers — not a quoted price, an offer,
        or investment advice. Figures are approximate.
      </p>
    </div>
  </div>
</body></html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description="SpaceX daily valuation estimate")
    parser.add_argument("--date", help="target date YYYY-MM-DD (default: today)")
    parser.add_argument("--format", choices=["text", "html"], default="text")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--shares", type=float, help="mark a holding of N shares (default: data/holdings.json)")
    parser.add_argument("--no-holdings", action="store_true", help="ignore data/holdings.json")
    args = parser.parse_args()

    target = _parse(args.date) if args.date else date.today()
    data = load_data()

    shares = args.shares
    if shares is None and not args.no_holdings:
        h = load_holdings()
        if h:
            shares = h.get("shares")

    if args.json:
        est = estimate_valuation(target, data)
        est["daily_change"] = daily_change(target, data)
        if shares:
            est["position"] = position(shares, target, data)
        print(json.dumps(est, indent=2, default=str))
        return

    digest = build_digest(target, data, shares=shares)
    print(render_html(digest) if args.format == "html" else render_text(digest))


if __name__ == "__main__":
    main()
