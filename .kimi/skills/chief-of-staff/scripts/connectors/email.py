#!/usr/bin/env python3
"""Gmail API connector with a graceful fallback stub."""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def fetch_email(config: dict) -> dict:
    """Return normalized email source JSON."""
    creds = os.getenv("GMAIL_CREDENTIALS") or os.getenv("GOOGLE_CREDENTIALS")
    token = os.getenv("GMAIL_TOKEN") or os.getenv("GOOGLE_TOKEN")

    fetched_at = datetime.now(timezone.utc).isoformat()

    if not (creds and token):
        return {
            "source": "email",
            "fetched_at": fetched_at,
            "configured": False,
            "note": "Gmail credentials not configured. Set GMAIL_CREDENTIALS and GMAIL_TOKEN (or GOOGLE_* equivalents).",
            "items": [
                {
                    "id": "email-not-configured",
                    "title": "Gmail not connected",
                    "summary": "No Gmail API credentials found in environment; using placeholder.",
                    "priority": 3,
                    "action_required": True,
                    "due": None,
                }
            ],
        }

    # Real Gmail API fetch would go here.
    return {
        "source": "email",
        "fetched_at": fetched_at,
        "configured": True,
        "items": [
            {
                "id": "msg-1",
                "title": "Example email from Gmail",
                "summary": "This is a stub result. Replace with real Gmail API call.",
                "priority": 2,
                "action_required": True,
                "due": None,
            }
        ],
    }


if __name__ == "__main__":
    print(json.dumps(fetch_email({}), indent=2))
