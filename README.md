# Chief of Staff for Kimi Code CLI

An open-source, personal AI chief of staff that runs inside Kimi Code CLI. It pulls from your inbox, calendar, tasks, web signals, and custom sources, then delivers a concise daily briefing with clear, approval-gated actions.

## What it does

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│    Email    │   │   Calendar  │   │    Tasks    │   │     Web     │   │    Custom   │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                 │                 │                 │
       └─────────────────┴─────────────────┴─────────────────┴─────────────────┘
                                          │
                                          ▼
                              ┌───────────────────────┐
                              │      Synthesizer      │
                              │  priorities + format  │
                              └───────────┬───────────┘
                                          │
                                          ▼
                              ┌───────────────────────┐
                              │       Delivery        │
                              │ terminal / Notion /   │
                              │ Slack / email / draft │
                              └───────────────────────┘
```

## Quick start

1. **Clone the repo** into your Kimi workspace: `git clone https://github.com/hartmut-ux/ai-chief-of-staff.git`
2. **Copy `.env.example` to `.env`** and fill in your keys and MCP names. Never commit `.env`.
3. **Install MCP servers** for Gmail, Calendar, Notion, and Slack (see `docs/setup.md`).
4. **Run `/chief-of-staff`** in Kimi Code CLI to generate your first briefing.
5. **Set your approval dial** in `config/chief_of_staff.toml` (draft → ask → auto).

## Project structure

```
.
├── AGENTS.md                     # Project-level instructions for Kimi
├── constitution.md               # Role, priorities, briefing format, tone
├── README.md                     # This file
├── LICENSE                       # MIT License
├── .env.example                  # Template for secrets and config
├── .gitignore                    # Excludes secrets, cache, and build artifacts
├── config/                       # Approval dial and source settings
├── .kimi/skills/chief-of-staff/  # Kimi skill definition and scripts
│   ├── SKILL.md
│   ├── references/
│   ├── assets/
│   └── scripts/
├── .github/                      # GitHub Actions workflow
├── memory/                       # Runtime memory, cache, history, output
│   ├── preferences.md
│   ├── source-cache/
│   ├── history/
│   └── output/
└── docs/
    ├── index.md                  # Lovable landing-page copy
    ├── setup.md                  # Step-by-step setup guide
    └── architecture.md           # Architecture and data-flow docs
```

## Approval dial

Every action category has an approval level in `config/chief_of_staff.toml`:

- **draft** — generate the message or update, show it to the user, do not send.
- **ask** — show the action and ask for explicit yes/no before executing.
- **auto** — execute without confirmation (use with care).

Default is `draft` for all delivery actions. The dial is per category: email replies, calendar edits, task creation, Slack posts, web publishing.

## Automation

Run the agent on your laptop or in the cloud:

- **Local cron**: schedule `kimi /chief-of-staff` via your OS cron or a scheduler like `launchd`/`systemd`.
- **GitHub Actions**: use the included workflow (`.github/workflows/daily-briefing.yml`) to run the briefing on a schedule and optionally post to Slack or Notion.

## Sell it / Productize

This project is released under the MIT License. You can:

- Resell it as a template or private setup service.
- Wrap it as a SaaS and charge for hosted orchestration.
- Customize it for executives, investors, or agencies.

A ready-to-import Lovable landing page lives in `docs/index.md`.

## Roadmap

- **Memory loop** — learn from approvals, rejections, and recurring tasks.
- **Drafted replies** — generate reply drafts for high-priority emails.
- **Time blocking** — propose and optionally write focus blocks into the calendar.
