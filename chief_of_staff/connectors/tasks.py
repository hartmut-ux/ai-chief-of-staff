#!/usr/bin/env python3
"""Notion tasks connector with graceful fallback."""

import json
import os
from datetime import datetime, timezone

import requests

NOTION_API_VERSION = "2022-06-28"
DATABASE_QUERY_URL = "https://api.notion.com/v1/databases/{database_id}/query"


def _extract_property(prop: dict | None):
    """Extract a usable Python value from a Notion property object."""
    if not prop:
        return None

    ptype = prop.get("type")
    if ptype == "title":
        return "".join(t.get("plain_text", "") for t in prop.get("title", []))
    if ptype == "rich_text":
        return "".join(t.get("plain_text", "") for t in prop.get("rich_text", []))
    if ptype == "select":
        return prop.get("select", {}).get("name")
    if ptype == "status":
        return prop.get("status", {}).get("name")
    if ptype == "date":
        return prop.get("date", {}).get("start")
    if ptype == "number":
        return prop.get("number")
    if ptype == "checkbox":
        return prop.get("checkbox")
    if ptype == "multi_select":
        return [opt.get("name") for opt in prop.get("multi_select", [])]
    return None


def _find_title(props: dict) -> str:
    """Find the title of a Notion page from its properties."""
    for prop in props.values():
        if prop.get("type") == "title":
            return _extract_property(prop) or "(untitled)"
    return "(untitled)"


def _to_priority(value) -> int:
    """Normalize a Notion priority value to an integer 1-4."""
    if isinstance(value, (int, float)):
        return max(1, min(4, int(value)))
    if isinstance(value, str):
        mapping = {
            "p1": 1,
            "high": 1,
            "p2": 2,
            "medium": 2,
            "p3": 3,
            "low": 3,
            "p4": 4,
            "none": 4,
        }
        return mapping.get(value.lower().strip(), 3)
    return 3


def fetch_tasks(config: dict) -> dict:
    """Return normalized tasks source JSON from a Notion database."""
    fetched_at = datetime.now(timezone.utc).isoformat()
    token = os.getenv("NOTION_TOKEN") or os.getenv("NOTION_API_KEY")
    database_id = os.getenv("NOTION_DATABASE_ID")

    if not (token and database_id):
        return {
            "source": "tasks",
            "fetched_at": fetched_at,
            "configured": False,
            "note": (
                "Notion tasks not configured. Set NOTION_TOKEN (integration secret) "
                "and NOTION_DATABASE_ID (the UUID of your tasks database). Share the "
                "database with your integration under Connections."
            ),
            "items": [],
            "errors": [],
        }

    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json",
    }

    try:
        url = DATABASE_QUERY_URL.format(database_id=database_id)
        response = requests.post(url, headers=headers, json={}, timeout=20)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])

        items = []
        for page in results:
            props = page.get("properties", {})
            title = _find_title(props)
            status = _extract_property(props.get("Status"))
            due = (
                _extract_property(props.get("Due"))
                or _extract_property(props.get("Due date"))
                or _extract_property(props.get("Date"))
            )
            priority = _to_priority(_extract_property(props.get("Priority")))

            if status and str(status).strip().lower() == "done":
                continue

            items.append(
                {
                    "id": page.get("id"),
                    "category": "task",
                    "title": title,
                    "summary": _extract_property(props.get("Description")) or "",
                    "status": status,
                    "due_at": due,
                    "priority": priority,
                    "action_required": status not in ("Done", "Archived", "Canceled"),
                    "due": due,
                }
            )

        return {
            "source": "tasks",
            "fetched_at": fetched_at,
            "configured": True,
            "items": items,
            "errors": [],
        }
    except Exception as exc:
        return {
            "source": "tasks",
            "fetched_at": fetched_at,
            "configured": True,
            "note": f"Notion API error: {exc}",
            "items": [],
            "errors": [str(exc)],
        }


if __name__ == "__main__":
    print(json.dumps(fetch_tasks({}), indent=2))
