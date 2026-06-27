#!/usr/bin/env python3
"""Google Calendar connector with OAuth2 and graceful fallback."""

import json
import os
from datetime import datetime, timedelta, timezone


def _load_calendar_service(creds_path: str, token_path: str):
    """Build an authenticated Google Calendar API service."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def _detect_conflicts(events: list[dict]) -> list[tuple[str, str]]:
    """Return pairs of event ids that overlap in time."""
    timed = [e for e in events if e.get("start_at") and e.get("end_at")]
    timed.sort(key=lambda e: e["start_at"])
    conflicts = []
    for i in range(len(timed) - 1):
        current_end = timed[i].get("end_at")
        next_start = timed[i + 1].get("start_at")
        if current_end and next_start and current_end > next_start:
            conflicts.append((timed[i]["id"], timed[i + 1]["id"]))
    return conflicts


def fetch_calendar(config: dict) -> dict:
    """Return normalized calendar source JSON."""
    fetched_at = datetime.now(timezone.utc).isoformat()
    creds_path = os.getenv("CALENDAR_CREDENTIALS") or os.getenv("GOOGLE_CREDENTIALS")
    token_path = os.getenv("CALENDAR_TOKEN") or os.getenv("GOOGLE_TOKEN")

    if not (creds_path and token_path):
        return {
            "source": "calendar",
            "fetched_at": fetched_at,
            "configured": False,
            "note": (
                "Google Calendar credentials not configured. Set CALENDAR_CREDENTIALS "
                "(path to credentials.json) and CALENDAR_TOKEN (path to token.json). "
                "You can reuse the same OAuth client as Gmail if it has the Calendar API "
                "enabled. The first run will write token.json."
            ),
            "items": [],
            "errors": [],
        }

    if not os.path.exists(creds_path):
        return {
            "source": "calendar",
            "fetched_at": fetched_at,
            "configured": False,
            "note": f"Calendar credentials file not found: {creds_path}",
            "items": [],
            "errors": [f"Credentials file missing: {creds_path}"],
        }

    try:
        service = _load_calendar_service(creds_path, token_path)
    except ImportError as exc:
        return {
            "source": "calendar",
            "fetched_at": fetched_at,
            "configured": False,
            "note": (
                "Google Calendar dependencies not installed. Run: "
                "pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client"
            ),
            "items": [],
            "errors": [str(exc)],
        }
    except Exception as exc:
        return {
            "source": "calendar",
            "fetched_at": fetched_at,
            "configured": True,
            "note": f"Could not authenticate Google Calendar: {exc}",
            "items": [],
            "errors": [str(exc)],
        }

    try:
        now = datetime.now(timezone.utc)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_of_day.isoformat(),
                timeMax=end_of_day.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        items = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            location = event.get("location", "")
            items.append(
                {
                    "id": event.get("id"),
                    "category": "calendar",
                    "summary": event.get("summary", "(no title)"),
                    "start_at": start,
                    "end_at": end,
                    "location": location,
                    "description": event.get("description", ""),
                    "title": event.get("summary", "(no title)"),
                    "priority": 2 if location else 3,
                    "action_required": False,
                    "due": start,
                }
            )

        conflicts = _detect_conflicts(items)
        conflict_ids = {eid for pair in conflicts for eid in pair}
        for item in items:
            item["has_conflict"] = item["id"] in conflict_ids

        return {
            "source": "calendar",
            "fetched_at": fetched_at,
            "configured": True,
            "items": items,
            "errors": [],
            "conflicts": conflicts,
        }
    except Exception as exc:
        return {
            "source": "calendar",
            "fetched_at": fetched_at,
            "configured": True,
            "note": f"Calendar API error: {exc}",
            "items": [],
            "errors": [str(exc)],
        }


if __name__ == "__main__":
    print(json.dumps(fetch_calendar({}), indent=2))
