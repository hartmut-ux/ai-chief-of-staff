# MCP Setup Guide

This guide walks you through creating the credentials and integrations needed for the Gmail, Google Calendar, Notion, and Slack MCP servers.

## Gmail OAuth2

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or use an existing one).
3. Enable the **Gmail API**:
   - APIs & Services → Library → search "Gmail API" → Enable.
4. Create OAuth2 credentials:
   - APIs & Services → Credentials → Create credentials → OAuth client ID.
   - Application type: **Desktop app**.
   - Download the JSON and save it as `config/gmail-credentials.json` in this repo.
5. Run the MCP server or auth helper once to generate `config/gmail-token.json`.
6. Set in `.env`:
   ```env
   GMAIL_MCP_NAME=gmail
   ```

> Keep `config/gmail-credentials.json` and `config/gmail-token.json` out of git. They are already ignored by `.gitignore`.

## Google Calendar OAuth2

1. In the same Google Cloud project, enable the **Google Calendar API**:
   - APIs & Services → Library → search "Google Calendar API" → Enable.
2. Create another OAuth client ID (or reuse the Gmail desktop app and add scopes).
3. Make sure the OAuth consent screen includes the `https://www.googleapis.com/auth/calendar.readonly` scope.
4. Download the credentials JSON and save it as `config/calendar-credentials.json`.
5. Authorize the app to produce `config/calendar-token.json`.
6. Set in `.env`:
   ```env
   CALENDAR_MCP_NAME=calendar
   ```

## Notion integration

1. Open [Notion integrations](https://www.notion.so/my-integrations) and click **New integration**.
2. Name it "Chief of Staff", choose the associated workspace, and click Submit.
3. Copy the **Internal Integration Token** and add it to `.env`:
   ```env
   NOTION_MCP_NAME=notion
   # Some MCP servers expect the token here as well:
   NOTION_TOKEN=secret_...
   ```
4. Open the Notion database you want to use and click **Share** → **Add connections** → select your integration.
5. Copy the database ID from the URL and add it to `.env`:
   ```env
   NOTION_DATABASE_ID=your-database-id
   ```

> Notion database URLs look like `https://www.notion.so/workspace/1234567890abcdef1234567890abcdef?v=...`. The 32-character string is the database ID.

## Adding MCP servers to Kimi Code CLI

After the credentials are in place, register each server in Kimi Code CLI:

```bash
kimi mcp add gmail      --command "npx -y @anthropic-ai/mcp-gmail"
kimi mcp add calendar   --command "npx -y @anthropic-ai/mcp-calendar"
kimi mcp add notion     --command "npx -y @anthropic-ai/mcp-notion"
kimi mcp add slack      --command "npx -y @anthropic-ai/mcp-slack"
```

Replace the package names with the actual MCP server packages you choose. Match the server names to the `*_MCP_NAME` values in `.env`.

For Claude Code and Codex CLI, use their respective MCP configuration files or commands:

- **Claude Code**: edit `~/.claude/claude_mcp_settings.json` or use the in-app MCP settings.
- **Codex CLI**: edit `~/.codex/config.json` and add the servers under `mcpServers`.

## Slack webhook

For Slack delivery, you need an incoming webhook URL:

1. Go to [Slack API apps](https://api.slack.com/apps) and create a new app.
2. Enable **Incoming Webhooks** and add one to your workspace/channel.
3. Copy the webhook URL and add it to `.env`:
   ```env
   SLACK_MCP_NAME=slack
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
   ```

## Troubleshooting

| Problem | Likely cause | Fix |
|---------|--------------|-----|
| `Token expired` | OAuth refresh token is stale | Re-run the auth helper to refresh `*-token.json`. |
| `Insufficient permissions` | OAuth scopes are missing | Add the required scope in the Google Cloud consent screen. |
| `Notion database not found` | Integration not shared with the database | Open the database page and add the integration under Share. |
| MCP server not found | Server name mismatch | Make sure `.env` `*_MCP_NAME` matches the registered server name exactly. |
| `channel_not_found` in Slack | Wrong webhook URL or channel | Re-create the incoming webhook and update `SLACK_WEBHOOK_URL`. |
| `.env` values ignored | File not loaded | Confirm `.env` is in the project root and restart your assistant / terminal. |
