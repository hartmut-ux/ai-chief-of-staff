#!/usr/bin/env python3
"""Google Calendar connector with a graceful fallback stub."""
import json
import os
from datetime import datetime, timezone


def fetch_calendar(config: dict) -> dict:
    """Return normalized calendar source JSON."""
    creds = os.getenv("GOOGLE_CREDENTIALS") or os.getenv("GMAIL_CREDENTIALS")
    token = os.getenv("GOOGLE_TOKEN") or os.getenv("GMAIL_TOKEN")

    fetched_at = datetime.now(timezone.utc).isoformat()

    if not (creds and token):
        return {
            "source": "calendar",
            "fetched_at": fetched_at,
            "configured": False,
            "note": "Google Calendar credentials not configured. Set GOOGLE_CREDENTIALS and GOOGLE_TOKEN.",
            "items": [
                {
                    "id": "cal-not-configured",
                    "title": "Google Calendar not connected",
                    "summary": "No Calendar API credentials found in environment; using placeholder.",
                    "priority": 3,
                    "action_required": True,
                    "due": None,
                }
            ],
        }

    # Real Calendar API fetch would go here.
    return {
        "source": "calendar",
        "fetched_at": fetched_at,
        "configured": True,
        "items": [
            {
                "id": "evt-1",
                "title": "Example calendar event",
                "summary": "This is a stub result. Replace with real Google Calendar API call.",
                "priority": 1,
                "action_required": True,
                "due": fetched_at,
            }
        ],
    }


if __name__ == "__main__":
    print(json.dumps(fetch_calendar({}), indent=2))
