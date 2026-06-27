"""Notion delivery driver via the Notion API."""

import os

import requests


def deliver(content: str, config: dict | None = None, auto_run: bool = False) -> dict:
    """Append the briefing as blocks to a Notion page."""
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
