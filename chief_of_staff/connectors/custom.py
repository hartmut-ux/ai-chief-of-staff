#!/usr/bin/env python3
"""Custom API connector with env-driven endpoint/key."""

import json
import os
from datetime import datetime, timezone

import requests


def fetch_custom(config: dict) -> dict:
    """Return normalized custom source JSON."""
    url = os.getenv("CUSTOM_API_URL") or config.get("sources", {}).get("custom", {}).get("endpoint", "")
    key = os.getenv("CUSTOM_API_KEY")
    fetched_at = datetime.now(timezone.utc).isoformat()

    if not url:
        return {
            "source": "custom",
            "fetched_at": fetched_at,
            "configured": False,
            "note": "Custom API not configured. Set CUSTOM_API_URL or sources.custom.endpoint.",
            "items": [
                {
                    "id": "custom-not-configured",
                    "title": "Custom API not connected",
                    "summary": "No custom API URL found; using placeholder.",
                    "priority": 3,
                    "action_required": True,
                }
            ],
        }

    headers = {}
    if key:
        headers["Authorization"] = f"Bearer {key}"

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        payload = response.json()

        items = []
        if isinstance(payload, list):
            for idx, item in enumerate(payload[:5], start=1):
                items.append(
                    {
                        "id": f"custom-{idx}",
                        "title": str(item.get("title", item.get("name", "Custom item"))),
                        "summary": str(item.get("summary", item.get("description", "")))[:300],
                        "priority": int(item.get("priority", 2)),
                        "action_required": bool(item.get("action_required", False)),
                    }
                )
        else:
            items.append(
                {
                    "id": "custom-1",
                    "title": "Custom API response",
                    "summary": str(payload)[:300],
                    "priority": 2,
                    "action_required": False,
                }
            )

        return {
            "source": "custom",
            "fetched_at": fetched_at,
            "configured": True,
            "items": items,
        }
    except Exception as exc:
        return {
            "source": "custom",
            "fetched_at": fetched_at,
            "configured": bool(url),
            "error": str(exc),
            "items": [],
        }


if __name__ == "__main__":
    print(json.dumps(fetch_custom({}), indent=2))
