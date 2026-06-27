# Setup Guide

One engine, three AI frontends. Follow the section for the assistant you use, then finish the shared configuration steps.

## 1. Clone the repo

```bash
git clone https://github.com/hartmut-ux/ai-chief-of-staff.git
cd ai-chief-of-staff
```

## 2. Run the interactive installer

```bash
python scripts/install.py
```

If your system does not have a `python` command, use `python3 scripts/install.py`.

The installer will:

- Ask which assistant you are setting up (Kimi / Claude / Codex).
- Check that the matching skill wrapper folder exists.
- Let you pick which sources and delivery channels to enable.
- Set the default approval level (we recommend `draft`).
- Create `.env` from `.env.example` if it does not exist.
- Write `config/chief_of_staff.toml` with your choices.

## 3. Per-assistant setup

### Kimi Code CLI

1. Install [Kimi Code CLI](https://www.moonshot.cn/kimi-cli) and verify it loads in your terminal or IDE.
2. Register the MCP servers listed below (see `mcp-setup.md` for details).
3. The Kimi skill lives at `.kimi/skills/chief-of-staff/SKILL.md`. If it is missing, create it from the Kimi wrapper template.
4. Invoke the skill with `/chief-of-staff`.

### Claude Code

1. Install [Claude Code](https://docs.anthropic.com/en/docs/agents/claude-code).
2. Place or create the Claude skill at `.claude/skills/chief-of-staff/SKILL.md`.
3. Register the MCP servers in Claude Code's MCP settings (see `mcp-setup.md`).
4. Invoke the skill by name: `chief-of-staff`.

### Codex CLI

1. Install [Codex CLI](https://github.com/openai/codex).
2. Place or create the Codex skill at `.codex/skills/chief-of-staff/SKILL.md`.
3. Register the MCP servers in Codex's configuration (see `mcp-setup.md`).
4. Invoke the skill by name: `chief-of-staff`.

## 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your API keys and MCP server names. Do not commit `.env`.

Required variables depend on your enabled sources/channels:

| Source / channel | Variables |
|------------------|-----------|
| Gmail / Calendar | `GMAIL_MCP_NAME`, `CALENDAR_MCP_NAME` |
| Notion tasks | `NOTION_MCP_NAME`, `NOTION_DATABASE_ID` |
| Slack delivery | `SLACK_MCP_NAME`, `SLACK_WEBHOOK_URL` |
| Email delivery | `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS`, `EMAIL_TO` |
| Telegram delivery | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` (see `telegram-setup.md`) |
| Custom source | `CUSTOM_API_URL`, `CUSTOM_API_KEY` |

## 5. Install MCP servers

Register the following MCP servers in your assistant:

- **Gmail** — for inbox access and draft replies.
- **Calendar** — for today's events and conflict detection.
- **Notion** — for task lists and briefing output.
- **Slack** — for optional delivery to a channel or DM.

Set the matching `*_MCP_NAME` values in `.env`. See `mcp-setup.md` for step-by-step OAuth and integration setup.

## 6. Configure the approval dial

The installer writes safe defaults, but you can edit `config/chief_of_staff.toml` directly:

```toml
[approval]
email = "draft"
calendar = "draft"
tasks = "draft"
web = "draft"
custom = "draft"
delivery = "draft"
```

Set each category to `draft`, `ask`, or `auto`.

## 7. Run your first briefing

From the terminal:

```bash
python -m chief_of_staff run --preview
```

Or via your assistant's skill command (`/chief-of-staff` in Kimi).

Review the output, approve or reject proposed actions, and update `memory/preferences.md` with any feedback.

## 8. Schedule it

- **Local**: add a cron job or `launchd`/`systemd` task that runs `python -m chief_of_staff run --preview`.
- **Cloud**: enable the GitHub Actions workflow in `.github/workflows/daily-briefing.yml` and set the repository secrets from `.env`.
