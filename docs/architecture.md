# Architecture

## Subagent-per-source design

Each source has its own subagent. This keeps credentials isolated, failures contained, and sources easy to add or remove.

| Subagent | Responsibility |
|----------|----------------|
| Email agent | Fetch inbox, score urgency, extract intent and requested action. |
| Calendar agent | Read today's events, detect conflicts, flag prep needs. |
| Tasks agent | Pull outstanding tasks, owners, due dates, blockers. |
| Web agent | Fetch news, signals, competitor mentions, relevance score. |
| Custom agent | Query user-defined APIs, RSS feeds, databases, spreadsheets. |

## Data flow

1. **Orchestrator** reads `constitution.md` and `memory/preferences.md`.
2. Each source agent returns a normalized JSON object.
3. **Synthesizer** merges results, applies priorities, and formats the briefing.
4. **Delivery agent** renders output and executes actions based on the approval dial.
5. Outputs are written to `memory/output/` and optionally to Notion, Slack, or email.

## JSON normalization

Every source agent returns:

```json
{
  "source": "email",
  "items": [
    {
      "id": "msg_001",
      "title": "Subject line",
      "sender": "name@example.com",
      "summary": "One-line summary",
      "urgency": 8,
      "relevance": 9,
      "proposed_action": "Reply to confirm meeting"
    }
  ]
}
```

## Synthesizer

The synthesizer:

- Drops items below relevance threshold.
- Ranks by priority: revenue → team → customers → deep work.
- Generates the top-3 priorities and proposed actions.
- Tags each action with an approval level from `config/chief_of_staff.toml`.

## Delivery

Delivery routes:

- Terminal markdown briefing (default).
- Notion page or database entry.
- Slack message or webhook.
- Email via SMTP.
- Draft replies in Gmail.

## Memory loop

- `memory/preferences.md` stores user preferences, recurring tasks, and learned rules.
- `memory/source-cache/` keeps raw source responses for debugging.
- `memory/history/` stores past briefings.
- The synthesizer and source agents read preferences at the start of each run.

## GitHub Actions cloud schedule

The workflow in `.github/workflows/briefing.yml` runs the briefing on a cron schedule. It uses repository secrets for all credentials and can post the result to Slack or Notion. Set `approval` categories to `auto` only for safe, read-only delivery actions in cloud runs.
