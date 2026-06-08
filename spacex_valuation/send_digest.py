"""Send the SpaceX daily valuation digest by email.

Stdlib-only (smtplib + email). Configure via environment variables so it can
run unattended from cron or GitHub Actions:

    SMTP_HOST     e.g. smtp.gmail.com
    SMTP_PORT     e.g. 587 (STARTTLS) or 465 (SSL)
    SMTP_USER     SMTP username / login
    SMTP_PASS     SMTP password or app password
    DIGEST_FROM   From: address (defaults to SMTP_USER)
    DIGEST_TO     comma-separated recipient list
    SMTP_SSL      "1" to use implicit SSL (port 465) instead of STARTTLS

Usage:
    python send_digest.py                 # send today's digest
    python send_digest.py --date 2026-06-08
    python send_digest.py --dry-run       # print, don't send

For Gmail: create an App Password (Google Account → Security → App passwords)
and use it as SMTP_PASS with SMTP_HOST=smtp.gmail.com, SMTP_PORT=587.
"""

from __future__ import annotations

import argparse
import os
import smtplib
import ssl
import sys
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from valuation import _parse, build_digest, load_data, render_html, render_text


def build_message(digest: dict, sender: str, recipients: list[str]) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = digest["subject"]
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(render_text(digest), "plain", "utf-8"))
    msg.attach(MIMEText(render_html(digest), "html", "utf-8"))
    return msg


def send(msg: MIMEMultipart, sender: str, recipients: list[str]) -> None:
    host = os.environ["SMTP_HOST"]
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASS")
    use_ssl = os.environ.get("SMTP_SSL") == "1" or port == 465

    if use_ssl:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            if user:
                server.login(user, password)
            server.sendmail(sender, recipients, msg.as_string())
    else:
        with smtplib.SMTP(host, port) as server:
            server.starttls(context=ssl.create_default_context())
            if user:
                server.login(user, password)
            server.sendmail(sender, recipients, msg.as_string())


def main() -> int:
    parser = argparse.ArgumentParser(description="Email the SpaceX daily valuation digest")
    parser.add_argument("--date", help="target date YYYY-MM-DD (default: today)")
    parser.add_argument("--dry-run", action="store_true", help="print the digest instead of sending")
    args = parser.parse_args()

    target = _parse(args.date) if args.date else date.today()
    digest = build_digest(target, load_data())

    sender = os.environ.get("DIGEST_FROM") or os.environ.get("SMTP_USER") or "spacex-valuation@localhost"
    recipients = [r.strip() for r in os.environ.get("DIGEST_TO", "").split(",") if r.strip()]

    if args.dry_run:
        print(f"Subject: {digest['subject']}")
        print(f"From: {sender}")
        print(f"To: {', '.join(recipients) or '(set DIGEST_TO)'}")
        print()
        print(render_text(digest))
        return 0

    if not recipients:
        print("ERROR: set DIGEST_TO to a comma-separated list of recipients.", file=sys.stderr)
        return 2
    if "SMTP_HOST" not in os.environ:
        print("ERROR: set SMTP_HOST (and SMTP_PORT/SMTP_USER/SMTP_PASS) to send.", file=sys.stderr)
        return 2

    msg = build_message(digest, sender, recipients)
    send(msg, sender, recipients)
    print(f"Sent: {digest['subject']} -> {', '.join(recipients)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
