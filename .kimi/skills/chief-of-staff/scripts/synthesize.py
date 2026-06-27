#!/usr/bin/env python3
"""Synthesize cached source data into a daily briefing."""
import json
from datetime import datetime, timezone
from pathlib import Path

import toml
from dotenv import load_dotenv
from jinja2 import Environment, BaseLoader

DEFAULT_TEMPLATE = """# Daily Briefing for {{ owner_name }}

Date: {{ date }}

## Top Priorities
{% for item in top_priorities %}
{{ loop.index }}. {% if item.action_required %}[ACTION]{% endif %} **{{ item.title }}**
   Source: {{ item.source }} | Priority: {{ item.priority }}
   {{ item.summary }}
{% else %}
No priorities found.
{% endfor %}

## Other Items
{% for item in other_items %}
- **{{ item.title }}** ({{ item.source }}, priority {{ item.priority }}) — {{ item.summary }}
{% else %}
No other items.
{% endfor %}

{% if preferences %}
## Active Preferences
{% for p in preferences %}
- {{ p }}
{% endfor %}
{% endif %}
"""


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[4]


def read_text_optional(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _parse_dt(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def _time_filter(value):
    dt = _parse_dt(value)
    return dt.strftime("%H:%M") if dt else str(value)


def _datetime_filter(value):
    dt = _parse_dt(value)
    return dt.strftime("%Y-%m-%d %H:%M") if dt else str(value)


def _jinja_env():
    env = Environment(loader=BaseLoader())
    env.filters["time"] = _time_filter
    env.filters["datetime"] = _datetime_filter
    return env


def load_cached_sources(root: Path):
    cache_dir = root / "memory" / "source-cache"
    sources = {}
    if not cache_dir.exists():
        return sources
    for path in sorted(cache_dir.glob("*.json")):
        try:
            sources[path.stem] = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
    return sources


def normalize_item(item: dict, source: str) -> dict:
    """Map a raw cached item to the fields the briefing template expects."""
    normalized = {
        "id": item.get("id", ""),
        "title": item.get("title", "Untitled"),
        "summary": item.get("summary", ""),
        "priority": item.get("priority", 3),
        "action_required": bool(item.get("action_required", False)),
        "source": item.get("source", source),
        "source_name": item.get("source_name", source),
        "link": item.get("url") or item.get("link"),
        "sender": item.get("sender"),
        "location": item.get("location"),
        "start_at": item.get("start_at") or item.get("due"),
        "end_at": item.get("end_at"),
        "due_at": item.get("due_at") or item.get("due"),
        "proposed_action": "Review and act" if item.get("action_required") else None,
    }
    return normalized


def build_template_context(sources: dict, config: dict, root: Path):
    owner = config.get("owner", {})
    approval = config.get("approval", {})

    inbox_items = [
        normalize_item(i, "email")
        for i in sources.get("email", {}).get("items", [])
    ]
    calendar_items = [
        normalize_item(i, "calendar")
        for i in sources.get("calendar", {}).get("items", [])
    ]
    task_items = [
        normalize_item(i, "tasks")
        for i in sources.get("tasks", {}).get("items", [])
    ]
    web_items = [
        normalize_item(i, "web")
        for i in sources.get("web", {}).get("items", [])
    ]
    custom_items = [
        normalize_item(i, "custom")
        for i in sources.get("custom", {}).get("items", [])
    ]

    all_items = inbox_items + calendar_items + task_items + web_items + custom_items
    sorted_items = sorted(
        all_items,
        key=lambda x: (x.get("priority", 99), not x.get("action_required", False)),
    )
    top_priorities = sorted_items[:3]

    proposed_actions = []
    for item in all_items:
        if item.get("action_required"):
            proposed_actions.append(
                {
                    "title": item["title"],
                    "source": item["source"],
                    "approval_status": approval.get(item["source"], "draft"),
                    "proposed_action": item.get("proposed_action", "Review"),
                }
            )

    errors = []
    for source_name, data in sources.items():
        if data.get("error"):
            errors.append(
                {
                    "source": source_name,
                    "message": data["error"],
                    "recoverable": True,
                }
            )
        elif data.get("configured") is False:
            errors.append(
                {
                    "source": source_name,
                    "message": data.get("note", "Source not configured"),
                    "recoverable": True,
                }
            )

    preferences = load_preferences(root)
    constitution = read_text_optional(root / "constitution.md") or read_text_optional(
        root / ".kimi" / "skills" / "chief-of-staff" / "references" / "constitution.md"
    )

    return {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "owner_name": owner.get("name", "Owner"),
        "user_name": owner.get("name", "Owner"),
        "top_priorities": top_priorities,
        "inbox_items": inbox_items,
        "calendar_items": calendar_items,
        "task_items": task_items,
        "web_items": web_items,
        "custom_items": custom_items,
        "proposed_actions": proposed_actions,
        "errors": errors,
        "preferences": preferences,
        "constitution": constitution,
        "sources": config.get("sources", {}).get("enabled", []),
        "other_items": sorted_items[3:],
    }


def load_preferences(root: Path):
    pref_path = root / "memory" / "preferences.md"
    if not pref_path.exists():
        return []
    rules = []
    for line in pref_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("-") or stripped.startswith("*"):
            rules.append(stripped.lstrip("- *").strip())
    return rules


def synthesize(config: dict | None = None, root: Path | None = None) -> tuple[Path, Path]:
    if root is None:
        root = get_project_root()
    if config is None:
        config = toml.load(root / "config" / "chief_of_staff.toml")

    sources = load_cached_sources(root)
    context = build_template_context(sources, config, root)

    template_path = (
        root
        / ".kimi"
        / "skills"
        / "chief-of-staff"
        / "references"
        / "briefing-template.md"
    )
    if template_path.exists():
        template_src = template_path.read_text(encoding="utf-8")
    else:
        template_src = DEFAULT_TEMPLATE

    env = _jinja_env()
    rendered = env.from_string(template_src).render(context)

    out_dir = root / "memory" / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    briefing_path = out_dir / "daily-briefing.md"
    briefing_path.write_text(rendered, encoding="utf-8")

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "owner": context["owner_name"],
        "total_items": sum(
            len(sources.get(name, {}).get("items", [])) for name in sources
        ),
        "top_priorities": [
            {
                "title": item.get("title"),
                "source": item.get("source"),
                "priority": item.get("priority"),
                "action_required": item.get("action_required"),
            }
            for item in context["top_priorities"]
        ],
        "proposed_actions_count": len(context["proposed_actions"]),
        "errors_count": len(context["errors"]),
        "preferences_count": len(context["preferences"]),
        "constitution_present": bool(context["constitution"]),
    }
    summary_path = out_dir / "briefing-summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    return briefing_path, summary_path


if __name__ == "__main__":
    root = get_project_root()
    env_path = root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    briefing, summary = synthesize()
    print(f"Briefing written to {briefing}")
    print(f"Summary written to {summary}")
