#!/usr/bin/env python3
"""Interactive installer for the AI-agnostic Chief of Staff engine.

Run with:
    python scripts/install.py

It configures the assistant frontend, enabled sources, delivery channels,
approval dial, and writes config/chief_of_staff.toml.
"""

from __future__ import annotations

import sys
from pathlib import Path

import toml

ROOT = Path(__file__).resolve().parents[1]

ASSISTANTS = {
    "kimi": ROOT / ".kimi" / "skills" / "chief-of-staff" / "SKILL.md",
    "claude": ROOT / ".claude" / "skills" / "chief-of-staff" / "SKILL.md",
    "codex": ROOT / ".codex" / "skills" / "chief-of-staff" / "SKILL.md",
}

SOURCE_OPTIONS = [
    ("email", "Gmail inbox (requires Gmail MCP / OAuth)"),
    ("calendar", "Google Calendar (requires Calendar MCP / OAuth)"),
    ("tasks", "Notion tasks (requires Notion integration)"),
    ("web", "Web signals (search / RSS / competitor mentions)"),
    ("custom", "Custom API or RSS feed"),
]

DELIVERY_OPTIONS = [
    ("console", "Terminal preview (always available)"),
    ("email", "Email via SMTP"),
    ("slack", "Slack message / webhook"),
    ("notion", "Notion page or database entry"),
    ("telegram", "Telegram bot message"),
]

APPROVAL_OPTIONS = [
    ("draft", "draft — show the briefing, do not send (recommended)"),
    ("ask", "ask — prompt before every outbound action"),
    ("auto", "auto — execute without confirmation (use with care)"),
]


def print_header(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def ask_choice(prompt: str, options: list[tuple[str, str]]) -> str:
    print(f"\n{prompt}")
    for idx, (key, label) in enumerate(options, start=1):
        print(f"  {idx}. {label}")
    while True:
        raw = input("Enter number: ").strip()
        if raw.isdigit():
            choice = int(raw)
            if 1 <= choice <= len(options):
                return options[choice - 1][0]
        print(f"Please enter a number between 1 and {len(options)}.")


def ask_checklist(prompt: str, options: list[tuple[str, str]]) -> list[str]:
    print(f"\n{prompt}")
    print("Enter the numbers you want to enable, separated by commas (e.g. 1,3,5).")
    for idx, (key, label) in enumerate(options, start=1):
        print(f"  {idx}. {label}")
    while True:
        raw = input("Enter numbers: ").strip()
        if not raw:
            return []
        keys = []
        valid = True
        for part in raw.split(","):
            part = part.strip()
            if not part.isdigit():
                valid = False
                break
            choice = int(part)
            if 1 <= choice <= len(options):
                keys.append(options[choice - 1][0])
            else:
                valid = False
                break
        if valid and keys:
            return keys
        print(f"Please enter a comma-separated list of numbers between 1 and {len(options)}.")


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    suffix = " [Y/n]: " if default else " [y/N]: "
    while True:
        raw = input(prompt + suffix).strip().lower()
        if not raw:
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("Please answer yes or no.")


def check_skill(assistant: str) -> None:
    path = ASSISTANTS[assistant]
    if path.exists():
        print(f"  ✓ Found {assistant} skill wrapper at {path}")
    else:
        print(f"  ⚠ WARNING: {assistant} skill wrapper not found at {path}")
        print("    You can still run the engine directly, but the AI assistant will not")
        print("    know how to invoke it. Copy or create the SKILL.md wrapper later.")


def ensure_env_file() -> None:
    env_path = ROOT / ".env"
    example_path = ROOT / ".env.example"

    if env_path.exists():
        print("  ✓ .env already exists — leaving it untouched.")
        return

    if example_path.exists():
        env_path.write_text(example_path.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"  ✓ Created {env_path} from {example_path}")
    else:
        env_path.write_text(
            "# Chief of Staff environment\n# Fill in real values. NEVER commit this file.\n",
            encoding="utf-8",
        )
        print(f"  ✓ Created empty {env_path}")

    print("\n  IMPORTANT: Open .env and fill in the credentials for every source")
    print("  and delivery channel you enabled. Never commit .env.")


def build_config(
    enabled_sources: list[str],
    enabled_delivery: list[str],
    approval: str,
) -> dict:
    """Build the chief_of_staff.toml config dict from installer choices."""
    primary_channel = enabled_delivery[0] if enabled_delivery else "console"

    config: dict = {
        "owner": {
            "name": "Owner",
            "timezone": "Europe/Zurich",
            "focus_hours_start": "09:00",
            "focus_hours_end": "17:00",
        },
        "sources": {
            "enabled": enabled_sources,
            "web": {"query": "AI agent chief of staff automation"},
            "custom": {"name": "Custom", "endpoint": ""},
        },
        "approval": {
            "email": approval,
            "calendar": approval,
            "tasks": approval,
            "web": approval,
            "custom": approval,
            "delivery": approval,
        },
        "delivery": {
            "channel": primary_channel,
            "channels": enabled_delivery,
            "email_to": "",
        },
    }
    return config


def write_config(config: dict) -> Path:
    config_path = ROOT / "config" / "chief_of_staff.toml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(toml.dumps(config), encoding="utf-8")
    return config_path


def print_next_steps(assistant: str, sources: list[str], delivery: list[str]) -> None:
    print_header("Next steps")
    print("1. Fill in the credentials in .env for the sources and channels you enabled.")
    if "slack" in delivery:
        print("   - Add SLACK_WEBHOOK_URL for Slack delivery.")
    if "email" in delivery:
        print("   - Add SMTP_HOST, SMTP_USER, SMTP_PASS, and EMAIL_TO for email delivery.")
    if "telegram" in delivery:
        print("   - Add TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID for Telegram delivery.")
    print("2. Wire up MCP servers. For Kimi Code CLI the commands look like:")
    print("     kimi mcp add gmail    --command \"npx -y @anthropic-ai/mcp-gmail\"")
    print("     kimi mcp add calendar --command \"npx -y @anthropic-ai/mcp-calendar\"")
    print("     kimi mcp add notion   --command \"npx -y @anthropic-ai/mcp-notion\"")
    print("     kimi mcp add slack    --command \"npx -y @anthropic-ai/mcp-slack\"")
    print("   See docs/mcp-setup.md for full OAuth and Claude/Codex instructions.")
    if "telegram" in delivery:
        print("3. Follow docs/telegram-setup.md to create a Telegram bot and get your chat ID.")
    print()
    print("4. Test the engine:")
    print("     python -m chief_of_staff run --preview")
    print()
    print(f"5. In {assistant}, invoke the skill with your wrapper command:")
    if assistant == "kimi":
        print("     /chief-of-staff")
    elif assistant == "claude":
        print("     Use the Claude skill at .claude/skills/chief-of-staff/")
    elif assistant == "codex":
        print("     Use the Codex skill at .codex/skills/chief-of-staff/")
    print()
    print("6. Tune memory/preferences.md and dial trusted sources up to ask/auto.")


def main() -> int:
    print_header("Chief of Staff — Interactive installer")
    print("This script generates config/chief_of_staff.toml and checks your setup.")

    assistant = ask_choice(
        "Which AI assistant are you setting up?",
        [("kimi", "Kimi Code CLI"), ("claude", "Claude / Claude Code"), ("codex", "Codex CLI")],
    )
    print(f"\nAssistant: {assistant}")
    check_skill(assistant)

    enabled_sources = ask_checklist("Which sources do you want to enable?", SOURCE_OPTIONS)
    print("Enabled sources:", ", ".join(enabled_sources) if enabled_sources else "none")

    enabled_delivery = ask_checklist(
        "Which delivery channels do you want to enable?",
        DELIVERY_OPTIONS,
    )
    print("Enabled delivery:", ", ".join(enabled_delivery) if enabled_delivery else "none")

    approval = ask_choice(
        "Choose the default approval level (we recommend draft):",
        APPROVAL_OPTIONS,
    )
    print(f"Default approval level: {approval}")

    print_header("Environment file")
    ensure_env_file()

    print_header("Writing configuration")
    config = build_config(enabled_sources, enabled_delivery, approval)
    config_path = write_config(config)
    print(f"  ✓ Wrote {config_path}")

    print_next_steps(assistant, enabled_sources, enabled_delivery)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled.")
        raise SystemExit(1)
