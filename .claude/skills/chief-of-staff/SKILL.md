---
name: chief-of-staff
description: Claude Code skill wrapper for the AI-agnostic chief_of_staff engine. Run a personal AI chief of staff that gathers email, calendar, tasks, web, and custom sources in parallel, synthesizes one prioritized daily briefing, and delivers it to your chosen channel.
---

# Chief of Staff — Claude wrapper

This is the **Claude Code skill wrapper** for the `chief_of_staff` Python engine. The skill is intentionally thin: all heavy logic lives in the top-level `chief_of_staff/` package. This wrapper only describes how to invoke the engine from Claude.

Use this skill when the user asks for:
- A daily briefing, morning rundown, or “what do I need to know today?”
- `/skill:chief-of-staff` or “run my chief of staff briefing”
- Coordination across email, calendar, tasks, news, or custom data feeds

## Workflow overview

The engine runs a **GATHER → SYNTHESIZE → DELIVER** pipeline.

```text
GATHER      SYNTHESIZE        DELIVER
  │              │                │
  ▼              ▼                ▼
sources  →  daily-briefing.md  →  console / email / Slack / Notion / Telegram
```

## Phase 1: GATHER

Option A — spawn parallel Claude subagents, one per enabled source. Each subagent:

1. Connects via its MCP server, API, or Claude built-in tool.
2. Fetches raw data for the configured window.
3. Normalizes every item to the schema in `chief_of_staff/references/connectors.md`.
4. Writes normalized JSON to `memory/source-cache/<source>.json`.

Option B — run the engine's gather stage directly (future flag):

```bash
python -m chief_of_staff run --gather-only
```

> **Note:** `--gather-only` is a planned CLI flag. Until the package implements it, run the full command `python -m chief_of_staff run --preview` and let the engine handle gather internally.

Supported sources:

| Source    | Typical connector                                    | Cache file                          |
|-----------|------------------------------------------------------|-------------------------------------|
| Email     | Gmail MCP, Outlook MCP, or IMAP script               | `memory/source-cache/email.json`    |
| Calendar  | Google Calendar MCP, Outlook Calendar MCP            | `memory/source-cache/calendar.json` |
| Tasks     | Notion MCP, Todoist MCP, Asana API, or local tasks   | `memory/source-cache/tasks.json`    |
| Web       | Claude web search or a custom scraping script        | `memory/source-cache/web.json`      |
| Custom    | User-provided API script or MCP                      | `memory/source-cache/custom.json`   |

> Do not block on any single source. If one connector is slow or fails, capture the error and continue.

## Phase 2: SYNTHESIZE

Run the synthesizer:

```bash
python -m chief_of_staff synthesize
```

The engine reads:

- All `memory/source-cache/*.json` files
- `constitution.md` (agent values, tone, boundaries)
- `config/chief_of_staff.toml` (approval dial, source settings)
- `memory/preferences.md` (user priorities, delivery rules, recurring context)

It produces `memory/output/daily-briefing.md` using the template at `chief_of_staff/references/briefing-template.md`. The output is ranked by priority, deduplicated, and time-aware.

## Phase 3: DELIVER

Always preview first:

```bash
python -m chief_of_staff deliver --preview
```

Then, after user approval, deliver to a channel:

```bash
python -m chief_of_staff deliver --channel slack
python -m chief_of_staff deliver --channel email
python -m chief_of_staff deliver --channel notion
python -m chief_of_staff deliver --channel telegram
```

Or run the full workflow in one command:

```bash
python -m chief_of_staff run --preview
python -m chief_of_staff run --channel slack
```

## Approval dial

Set the approval dial in `config/chief_of_staff.toml`:

```toml
[approval]
email = "draft"
calendar = "draft"
tasks = "draft"
web = "draft"
custom = "draft"
delivery = "draft"
```

| Level   | Behavior                                                    |
|---------|-------------------------------------------------------------|
| `draft` | Show the briefing only. Do not send.                        |
| `ask`   | Show the briefing and prompt the user before sending.       |
| `auto`  | Deliver to the configured channel without extra prompting.  |

- **Default for the first week:** everything `draft`.
- Only switch a source/category to `auto` after the user has validated its output at least once.
- Per-item overrides can be embedded in the briefing under `## Proposed Actions`.

## Error handling

- If a source fails, the gatherer writes an `errors` array to its cache file and continues.
- The synthesizer surfaces failed sources in `## Source Health` of the briefing.
- A delivery failure is logged and reported back to the user; no silent drops.

## Quick start

1. Configure MCP servers / API credentials for each source you want enabled.
2. Set the approval dial in `config/chief_of_staff.toml` to safe defaults (`draft`).
3. Run `python -m chief_of_staff run --preview` and review the first briefing.
4. Tune `memory/preferences.md`, then dial trusted sources up to `ask` or `auto`.

## References

- `chief_of_staff/references/connectors.md` — source connectors, raw shapes, normalized JSON schema, examples
- `chief_of_staff/references/briefing-template.md` — markdown briefing template
- `chief_of_staff/assets/briefing.html.j2` — HTML/Jinja2 rendering template
