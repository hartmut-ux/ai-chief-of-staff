#!/usr/bin/env python3
"""Notion tasks connector with a graceful fallback stub."""
import json
import os
from datetime import datetime, timezone


def fetch_tasks(config: dict) -> dict:
    """Return normalized tasks source JSON."""
    token = os.getenv("NOTION_TOKEN") or os.getenv("NOTION_API_KEY")
    database_id = os.getenv("NOTION_DATABASE_ID")

    fetched_at = datetime.now(timezone.utc).isoformat()

    if not (token and database_id):
        return {
            "source": "tasks",
            "fetched_at": fetched_at,
            "configured": False,
            "note": "Notion tasks not configured. Set NOTION_TOKEN and NOTION_DATABASE_ID.",
            "items": [
                {
                    "id": "tasks-not-configured",
                    "title": "Notion tasks not connected",
                    "summary": "No Notion API credentials found in environment; using placeholder.",
                    "priority": 3,
                    "action_required": True,
                    "due": None,
                }
            ],
        }

    # Real Notion API fetch would go here.
    return {
        "source": "tasks",
        "fetched_at": fetched_at,
        "configured": True,
        "items": [
            {
                "id": "task-1",
                "title": "Example task from Notion",
                "summary": "This is a stub result. Replace with real Notion API call.",
                "priority": 1,
                "action_required": True,
                "due": None,
            }
        ],
    }


if __name__ == "__main__":
    print(json.dumps(fetch_tasks({}), indent=2))
