"""Memory management for preferences, feedback, and decisions."""

from datetime import datetime, timezone
from pathlib import Path

from . import get_project_root


def preferences_path(root: Path | None = None) -> Path:
    """Return the path to memory/preferences.md."""
    if root is None:
        root = get_project_root()
    return root / "memory" / "preferences.md"


def load_preferences(root: Path | None = None) -> list[str]:
    """Read preference rules from memory/preferences.md."""
    path = preferences_path(root)
    if not path.exists():
        return []
    rules = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("-") or stripped.startswith("*"):
            rules.append(stripped.lstrip("- *").strip())
    return rules


def append_feedback(feedback_text: str, run_date: str | None = None, root: Path | None = None) -> Path:
    """Append a feedback entry to memory/preferences.md."""
    path = preferences_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("# User Preferences & Feedback\n\n", encoding="utf-8")

    date = run_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    entry = f"\n## Feedback — {date}\n\n- {feedback_text}\n"
    with path.open("a", encoding="utf-8") as f:
        f.write(entry)
    return path


def record_decision(category: str, decision: str, root: Path | None = None) -> Path:
    """Append an ignore/escalate rule to memory/preferences.md."""
    path = preferences_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("# User Preferences & Feedback\n\n", encoding="utf-8")

    entry = f"\n- [{category.upper()}] {decision}\n"
    with path.open("a", encoding="utf-8") as f:
        f.write(entry)
    return path
