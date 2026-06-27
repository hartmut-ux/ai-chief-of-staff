"""Telegram delivery driver via the Telegram Bot API."""

import os

import requests

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"
MAX_MESSAGE_LENGTH = 4000


def _split_content(content: str, max_len: int = MAX_MESSAGE_LENGTH) -> list[str]:
    """Split long content into Telegram-friendly chunks."""
    if len(content) <= max_len:
        return [content]

    parts = []
    remaining = content
    while remaining:
        if len(remaining) <= max_len:
            parts.append(remaining)
            break

        # Prefer splitting on a newline to keep formatting clean.
        split_at = remaining.rfind("\n", 0, max_len)
        if split_at <= 0:
            split_at = max_len
        parts.append(remaining[:split_at])
        remaining = remaining[split_at:].lstrip()

    return parts


def deliver_telegram(content: str, config: dict | None = None) -> dict:
    """Send the briefing via Telegram Bot API, splitting if necessary."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token:
        return {
            "channel": "telegram",
            "status": "failed",
            "error": "TELEGRAM_BOT_TOKEN not set.",
        }
    if not chat_id:
        return {
            "channel": "telegram",
            "status": "failed",
            "error": "TELEGRAM_CHAT_ID not set.",
        }

    cfg = config or {}
    parse_mode = cfg.get("delivery", {}).get("telegram", {}).get("parse_mode", "Markdown")
    parts = _split_content(content)
    message_ids = []
    errors = []

    for part in parts:
        try:
            url = TELEGRAM_API_URL.format(token=token)
            payload = {
                "chat_id": chat_id,
                "text": part,
            }
            if parse_mode:
                payload["parse_mode"] = parse_mode
            response = requests.post(url, json=payload, timeout=20)
            response.raise_for_status()
            result = response.json().get("result", {})
            message_ids.append(result.get("message_id"))
        except Exception as exc:
            errors.append(str(exc))

    if errors:
        return {
            "channel": "telegram",
            "status": "partial" if message_ids else "failed",
            "message_ids": message_ids,
            "parts": len(parts),
            "errors": errors,
        }

    return {
        "channel": "telegram",
        "status": "success",
        "message_ids": message_ids,
        "parts": len(parts),
    }


def deliver(content: str, config: dict | None = None, auto_run: bool = False) -> dict:
    """Adapter exposing the same signature as the other delivery drivers."""
    return deliver_telegram(content, config)
