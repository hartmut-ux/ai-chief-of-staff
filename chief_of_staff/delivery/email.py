"""Email delivery driver via SMTP."""

import os
import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage


def deliver(content: str, config: dict | None = None, auto_run: bool = False) -> dict:
    """Send the briefing by email."""
    cfg = (config or {}).get("delivery", {})
    to = os.getenv("EMAIL_TO") or cfg.get("email_to", "")
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD") or os.getenv("SMTP_PASS")

    if not all([to, smtp_user, smtp_pass]):
        return {
            "channel": "email",
            "status": "failed",
            "error": "Missing SMTP_USER, SMTP_PASSWORD, or EMAIL_TO.",
        }

    msg = EmailMessage()
    msg["Subject"] = f"Daily Briefing — {datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
    msg["From"] = smtp_user
    msg["To"] = to
    msg.set_content(content)

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        return {"channel": "email", "status": "success", "to": to}
    except Exception as exc:
        return {"channel": "email", "status": "failed", "error": str(exc)}
