#!/usr/bin/env python3
"""Web search connector with optional Serper/Bing API or stub fallback."""
import json
import os
from datetime import datetime, timezone

import requests


def fetch_web(config: dict) -> dict:
    """Return normalized web source JSON."""
    query = (
        config.get("sources", {}).get("web", {}).get(
            "query", "AI agent chief of staff automation"
        )
    )
    fetched_at = datetime.now(timezone.utc).isoformat()

    api_key = os.getenv("SERPER_API_KEY") or os.getenv("BING_API_KEY") or os.getenv("SEARCH_API_KEY")

    if api_key:
        try:
            if os.getenv("SERPER_API_KEY"):
                url = "https://google.serper.dev/search"
                headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
                payload = {"q": query, "num": 5}
                response = requests.post(url, json=payload, headers=headers, timeout=20)
            else:
                # Generic Bing-style fallback shape
                url = "https://api.bing.microsoft.com/v7.0/search"
                headers = {"Ocp-Apim-Subscription-Key": api_key}
                response = requests.get(url, params={"q": query, "count": 5}, headers=headers, timeout=20)

            response.raise_for_status()
            data = response.json()

            items = []
            organic = data.get("organic", []) or data.get("webPages", {}).get("value", [])
            for idx, result in enumerate(organic[:5], start=1):
                items.append(
                    {
                        "id": f"web-{idx}",
                        "title": result.get("title", "No title"),
                        "summary": result.get("snippet", result.get("snippet", "")),
                        "url": result.get("link", result.get("url", "")),
                        "priority": 2,
                        "action_required": False,
                    }
                )

            return {
                "source": "web",
                "fetched_at": fetched_at,
                "configured": True,
                "query": query,
                "items": items,
            }
        except Exception as exc:
            return {
                "source": "web",
                "fetched_at": fetched_at,
                "configured": True,
                "error": str(exc),
                "items": [],
            }

    # No search service configured: return a stub item so the pipeline still works.
    return {
        "source": "web",
        "fetched_at": fetched_at,
        "configured": False,
        "note": "No search API configured. Set SERPER_API_KEY or BING_API_KEY for live results.",
        "query": query,
        "items": [
            {
                "id": "web-1",
                "title": f"Example web result for '{query}'",
                "summary": "This is a placeholder because no search API key is configured.",
                "url": "#",
                "priority": 2,
                "action_required": False,
            }
        ],
    }


if __name__ == "__main__":
    print(json.dumps(fetch_web({}), indent=2))
