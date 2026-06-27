"""Slack delivery driver via webhook."""

import os

import requests


def deliver(content: str, config: dict | None = None, auto_run: bool = False) -> dict:
    """Post the briefing to a Slack webhook."""
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
