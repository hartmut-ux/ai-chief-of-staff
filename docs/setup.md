# Setup Guide

## 1. Install Kimi Code CLI

Follow the official Kimi Code CLI installation guide and verify it loads in your terminal or IDE.

## 2. Clone the repo

```bash
git clone https://github.com/your-org/chief-of-staff-kimi.git
cd chief-of-staff-kimi
```

## 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your API keys and MCP server names. Do not commit `.env`.

## 4. Install MCP servers

Register the following MCP servers in Kimi Code CLI:

- **Gmail** — for inbox access and draft replies.
- **Calendar** — for today's events and conflict detection.
- **Notion** — for task lists and briefing output.
- **Slack** — for optional delivery to a channel or DM.

Set the matching `*_MCP_NAME` values in `.env`.

## 5. Configure the approval dial

Edit `config/chief_of_staff.toml` and set each category to `draft`, `ask`, or `auto`:

```toml
[approval]
email_replies = "draft"
calendar_edits = "ask"
task_creation = "ask"
slack_posts = "draft"
web_publishing = "draft"
```

## 6. Run your first briefing

In Kimi Code CLI:

```
/chief-of-staff
```

Review the output, approve or reject proposed actions, and update `memory/preferences.md` with any feedback.

## 7. Schedule it

- **Local**: add a cron job or `launchd`/`systemd` task that runs `kimi /chief-of-staff`.
- **Cloud**: enable the GitHub Actions workflow in `.github/workflows/briefing.yml` and set the repository secrets from `.env`.
