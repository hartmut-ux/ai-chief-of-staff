#!/usr/bin/env python3
"""Gmail API connector with OAuth2 and graceful fallback."""

import json
import os
from datetime import datetime, timedelta, timezone


def _priority_from_email(sender: str, subject: str, snippet: str) -> int:
    """Heuristic priority based on sender domain and content keywords."""
    text = f"{sender} {subject} {snippet}".lower()
    urgent = ["urgent", "asap", "action required", "immediate", "failure", "alert", "security"]
    high = ["stripe", "invoice", "billing", "payment", "customer", "support", "escalation", "deadline"]
    medium = ["meeting", "reminder", "update", "newsletter"]
    if any(k in text for k in urgent):
        return 1
    if any(k in text for k in high):
        return 2
    if any(k in text for k in medium):
        return 3
    return 4


def _load_gmail_service(creds_path: str, token_path: str):
    """Build an authenticated Gmail API service."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

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

    return build("gmail", "v1", credentials=creds)


def fetch_email(config: dict) -> dict:
    """Return normalized email source JSON."""
    fetched_at = datetime.now(timezone.utc).isoformat()
    creds_path = os.getenv("GMAIL_CREDENTIALS") or os.getenv("GOOGLE_CREDENTIALS")
    token_path = os.getenv("GMAIL_TOKEN") or os.getenv("GOOGLE_TOKEN")

    if not (creds_path and token_path):
        return {
            "source": "email",
            "fetched_at": fetched_at,
            "configured": False,
            "note": (
                "Gmail credentials not configured. Set GMAIL_CREDENTIALS (path to "
                "credentials.json) and GMAIL_TOKEN (path to token.json). You can "
                "download credentials.json from Google Cloud Console > APIs & Services > "
                "Credentials > OAuth 2.0 Client IDs. The first run will write token.json."
            ),
            "items": [],
            "errors": [],
        }

    if not os.path.exists(creds_path):
        return {
            "source": "email",
            "fetched_at": fetched_at,
            "configured": False,
            "note": f"Gmail credentials file not found: {creds_path}",
            "items": [],
            "errors": [f"Credentials file missing: {creds_path}"],
        }

    try:
        service = _load_gmail_service(creds_path, token_path)
    except ImportError as exc:
        return {
            "source": "email",
            "fetched_at": fetched_at,
            "configured": False,
            "note": (
                "Gmail dependencies not installed. Run: "
                "pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client"
            ),
            "items": [],
            "errors": [str(exc)],
        }
    except Exception as exc:
        return {
            "source": "email",
            "fetched_at": fetched_at,
            "configured": True,
            "note": f"Could not authenticate Gmail: {exc}",
            "items": [],
            "errors": [str(exc)],
        }

    try:
        since = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y/%m/%d")
        query = f"is:unread in:inbox after:{since}"
        results = service.users().messages().list(userId="me", q=query, maxResults=20).execute()
        messages = results.get("messages", [])

        items = []
        for msg in messages:
            msg_data = (
                service.users()
                .messages()
                .get(
                    userId="me",
                    id=msg["id"],
                    format="metadata",
                    metadataHeaders=["From", "Subject"],
                )
                .execute()
            )
            headers = {
                h["name"].lower(): h["value"]
                for h in msg_data.get("payload", {}).get("headers", [])
            }
            sender = headers.get("from", "Unknown")
            subject = headers.get("subject", "(no subject)")
            snippet = msg_data.get("snippet", "")
            internal_date = msg_data.get("internalDate")

            items.append(
                {
                    "id": msg["id"],
                    "category": "inbox",
                    "sender": sender,
                    "subject": subject,
                    "snippet": snippet,
                    "internalDate": internal_date,
                    "title": subject,
                    "summary": snippet,
                    "priority": _priority_from_email(sender, subject, snippet),
                    "action_required": True,
                    "due": None,
                }
            )

        return {
            "source": "email",
            "fetched_at": fetched_at,
            "configured": True,
            "items": items,
            "errors": [],
        }
    except Exception as exc:
        return {
            "source": "email",
            "fetched_at": fetched_at,
            "configured": True,
            "note": f"Gmail API error: {exc}",
            "items": [],
            "errors": [str(exc)],
        }


if __name__ == "__main__":
    print(json.dumps(fetch_email({}), indent=2))
