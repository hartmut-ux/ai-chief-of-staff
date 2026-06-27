---
name: chief-of-staff
description: Run a personal AI chief of staff inside Kimi Code CLI. Gather email, calendar, tasks, web, and custom sources in parallel, synthesize one prioritized daily briefing, and deliver it to email/Slack/Notion. Use when the user asks for a daily briefing, runs /chief-of-staff, or wants to coordinate their routine.
---

# Chief of Staff

A personal AI chief of staff for Kimi Code CLI. It runs a daily **GATHER → SYNTHESIZE → DELIVER** workflow, pulls signals from your tools and the web, and produces a single prioritized briefing with proposed actions.

Use this skill when the user asks for:
- A daily briefing, morning rundown, or “what do I need to know today?”
- `/chief-of-staff` or `/skill:chief-of-staff`
- Coordination across email, calendar, tasks, news, or custom data feeds

## 3-Phase Workflow

### Phase 1: GATHER

Spawn parallel subagents, one per source. Each subagent:

1. Connects via its MCP server, API, or Kimi built-in tool.
2. Fetches raw data for the relevant window (e.g., unread email since yesterday, today’s calendar, open tasks).
3. Normalizes every item to the schema in `references/connectors.md`.
4. Writes normalized JSON to `memory/source-cache/<source>.json`.

Supported sources:

| Source    | Typical connector                                    | Cache file                          |
|-----------|------------------------------------------------------|-------------------------------------|
| Email     | Gmail MCP, Outlook MCP, or IMAP script               | `memory/source-cache/email.json`    |
| Calendar  | Google Calendar MCP, Outlook Calendar MCP            | `memory/source-cache/calendar.json` |
| Tasks     | Notion MCP, Todoist MCP, Asana API, or local tasks   | `memory/source-cache/tasks.json`    |
| Web       | Kimi `SearchWeb` / `FetchURL`                        | `memory/source-cache/web.json`      |
| Custom    | User-provided API script or MCP                      | `memory/source-cache/custom.json`   |

> **Note:** Do not block on any single source. If one connector is slow or fails, capture the error and continue.

### Phase 2: SYNTHESIZE

Run the synthesizer:

```bash
python .kimi/skills/chief-of-staff/scripts/synthesize.py
```

The script (or a synthesizer subagent) reads:

- All `memory/source-cache/*.json` files
- `constitution.md` (agent values, tone, boundaries)
- `config/chief_of_staff.toml` (approval dial, source settings)
- `memory/preferences.md` (user priorities, delivery rules, recurring context)

It produces `memory/output/daily-briefing.md` using the template at `references/briefing-template.md`. The output is ranked by priority, deduplicated, and time-aware.

### Phase 3: DELIVER

Always preview first:

```bash
python .kimi/skills/chief-of-staff/scripts/deliver.py --preview
```

Then apply the approval dial:

| Level  | Behavior                                                    |
|--------|-------------------------------------------------------------|
| `draft` | Show the briefing only. Do not send.                        |
| `ask`   | Show the briefing and prompt the user before sending.       |
| `auto`  | Deliver to the configured channel without extra prompting.  |

If the user confirms (or the dial is `auto`), deliver via the configured channel (email, Slack, Notion, etc.). The HTML rendering can use `assets/briefing.html.j2`.

After delivery, ask the user for feedback and append it to `memory/preferences.md` via `memory_manager.py`.

## Approval Dial

Each source and category can be configured independently:

```yaml
approval_dial:
  default: draft
  email: ask
  calendar: draft
  tasks: ask
  web: draft
  custom: ask
```

- **Default for the first week:** everything `draft`.
- Only switch a source/category to `auto` after the user has validated its output at least once.
- Per-item overrides can be embedded in the briefing under `## Proposed Actions`.

## Error Handling

- If a source fails, the gatherer writes an `errors` array to its cache file and continues.
- The synthesizer surfaces failed sources in `## Source Health` of the briefing.
- A delivery failure is logged and reported back to the user; no silent drops.

## Quick Start

1. Configure MCP servers / API credentials for each source you want enabled.
2. Set the approval dial in `config/chief_of_staff.toml` to safe defaults (`draft`).
3. Run `/chief-of-staff` and review the first briefing.
4. Tune preferences, then dial trusted sources up to `ask` or `auto`.

## References

- `references/connectors.md` — source connectors, raw shapes, normalized JSON schema, examples
- `references/briefing-template.md` — markdown briefing template
- `assets/briefing.html.j2` — HTML/Jinja2 rendering template
