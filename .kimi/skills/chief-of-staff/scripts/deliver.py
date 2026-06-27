#!/usr/bin/env python3
"""Deliver the generated daily briefing to the chosen channel."""
import argparse
import json
import os
import smtplib
import sys
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path

import requests
import toml


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[4]


def load_config(root: Path) -> dict:
    return toml.load(root / "config" / "chief_of_staff.toml")


def log_delivery(root: Path, entry: dict) -> None:
    log_path = root / "memory" / "output" / "delivery-log.json"
    logs = []
    if log_path.exists():
        try:
            logs = json.loads(log_path.read_text(encoding="utf-8"))
            if not isinstance(logs, list):
                logs = [logs]
        except Exception:
            logs = []
    logs.append(entry)
    log_path.write_text(json.dumps(logs, indent=2, ensure_ascii=False), encoding="utf-8")


def deliver_console(root: Path, content: str, auto_run: bool):
    print(content)
    return {"channel": "console", "status": "success", "note": "printed to stdout"}


def deliver_email(root: Path, content: str, auto_run: bool):
    cfg = load_config(root).get("delivery", {})
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


def deliver_slack(root: Path, content: str, auto_run: bool):
    webhook = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook:
        return {
            "channel": "slack",
            "status": "failed",
            "error": "SLACK_WEBHOOK_URL not set.",
        }
    payload = {"text": content[:2000]}
    try:
        response = requests.post(webhook, json=payload, timeout=20)
        response.raise_for_status()
        return {"channel": "slack", "status": "success"}
    except Exception as exc:
        return {"channel": "slack", "status": "failed", "error": str(exc)}


def deliver_notion(root: Path, content: str, auto_run: bool):
    token = os.getenv("NOTION_TOKEN")
    page_id = os.getenv("NOTION_BRIEFING_PAGE_ID")
    if not (token and page_id):
        return {
            "channel": "notion",
            "status": "failed",
            "error": "NOTION_TOKEN or NOTION_BRIEFING_PAGE_ID not set.",
        }

    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    children = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": line}}]
            },
        }
        for line in content.splitlines()
        if line.strip()
    ]
    try:
        response = requests.patch(url, headers=headers, json={"children": children}, timeout=20)
        response.raise_for_status()
        return {"channel": "notion", "status": "success", "page_id": page_id}
    except Exception as exc:
        return {"channel": "notion", "status": "failed", "error": str(exc)}


def deliver(
    root: Path | None = None,
    channel: str | None = None,
    preview: bool = True,
    auto_run: bool = False,
) -> dict:
    if root is None:
        root = get_project_root()

    briefing_path = root / "memory" / "output" / "daily-briefing.md"
    if not briefing_path.exists():
        entry = {
            "channel": channel or "preview",
            "status": "failed",
            "error": "Briefing not found.",
        }
        log_delivery(root, entry)
        return entry

    content = briefing_path.read_text(encoding="utf-8")

    if preview or not channel:
        result = deliver_console(root, content, auto_run)
        result["channel"] = "preview"
    elif channel == "console":
        result = deliver_console(root, content, auto_run)
    elif channel == "email":
        result = deliver_email(root, content, auto_run)
    elif channel == "slack":
        result = deliver_slack(root, content, auto_run)
    elif channel == "notion":
        result = deliver_notion(root, content, auto_run)
    else:
        result = {"channel": channel, "status": "failed", "error": "Unknown channel."}

    result["delivered_at"] = datetime.now(timezone.utc).isoformat()
    log_delivery(root, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Deliver the daily briefing.")
    parser.add_argument(
        "--preview",
        action="store_true",
        default=True,
        help="Preview the briefing on stdout (default).",
    )
    parser.add_argument(
        "--channel",
        choices=["console", "email", "slack", "notion"],
        help="Delivery channel.",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Run without interactive approval prompts.",
    )
    args = parser.parse_args()

    root = get_project_root()
    preview = args.preview if not args.channel else False
    result = deliver(root, channel=args.channel, preview=preview, auto_run=args.auto)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
