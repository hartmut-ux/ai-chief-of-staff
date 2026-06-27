"""Delivery channels for the generated briefing."""

import json
from datetime import datetime, timezone
from pathlib import Path

from .. import get_project_root

from .console import deliver as deliver_console
from .email import deliver as deliver_email
from .notion import deliver as deliver_notion
from .slack import deliver as deliver_slack
from .telegram import deliver as deliver_telegram


CHANNELS = {
    "console": deliver_console,
    "email": deliver_email,
    "slack": deliver_slack,
    "notion": deliver_notion,
    "telegram": deliver_telegram,
}


def log_delivery(root: Path, entry: dict) -> None:
    """Append a delivery log entry to memory/output/delivery-log.json."""
    log_path = root / "memory" / "output" / "delivery-log.json"
    logs = []
    if log_path.exists():
        try:
            logs = json.loads(log_path.read_text(encoding="utf-8"))
            if not isinstance(logs, list):
                logs = [logs]
        except Exception:
            logs = []
    logs.append(entry)
    log_path.write_text(json.dumps(logs, indent=2, ensure_ascii=False), encoding="utf-8")


def deliver(
    channel: str | None = None,
    preview: bool = True,
    auto_run: bool = False,
    config: dict | None = None,
    root: Path | None = None,
) -> dict:
    """Deliver the generated briefing to the chosen channel."""
    if root is None:
        root = get_project_root()

    briefing_path = root / "memory" / "output" / "daily-briefing.md"
    if not briefing_path.exists():
        entry = {
            "channel": channel or "preview",
            "status": "failed",
            "error": "Briefing not found.",
        }
        log_delivery(root, entry)
        return entry

    content = briefing_path.read_text(encoding="utf-8")

    if preview or not channel:
        result = deliver_console(content, config, auto_run)
        result["channel"] = "preview"
    elif channel in CHANNELS:
        result = CHANNELS[channel](content, config, auto_run)
    else:
        result = {"channel": channel, "status": "failed", "error": "Unknown channel."}

    result["delivered_at"] = datetime.now(timezone.utc).isoformat()
    log_delivery(root, result)
    return result
