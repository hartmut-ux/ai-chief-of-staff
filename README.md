# Chief of Staff for Kimi, Claude & Codex

An open-source, personal AI chief of staff that runs inside **Kimi Code CLI**, **Claude Code**, or **Codex**. It pulls from your inbox, calendar, tasks, web signals, and custom sources, then delivers a concise daily briefing with clear, approval-gated actions.

**Live page:** https://hartmut-ux.github.io/ai-chief-of-staff

One AI-agnostic engine (`chief_of_staff/`) powers all three frontends. Thin skill wrappers in `.kimi/`, `.claude/`, and `.codex/` teach each assistant how to invoke it.

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
                             │   chief_of_staff/     │
                             │  gather · synthesize  │
                             └───────────┬───────────┘
                                         │
                                         ▼
                             ┌───────────────────────┐
                             │       Delivery        │
                             │  console / email /    │
                             │  slack / notion /     │
                             │  telegram             │
                             └───────────────────────┘
```

## Supported AI frontends

| Assistant | Skill path | Invoke command |
|-----------|------------|----------------|
| **Kimi Code CLI** | `.kimi/skills/chief-of-staff/` | `/chief-of-staff` |
| **Claude Code** | `.claude/skills/chief-of-staff/` | Skill name: `chief-of-staff` |
| **Codex CLI** | `.codex/skills/chief-of-staff/` | Skill name: `chief-of-staff` |

The same engine runs underneath every frontend, so your configuration and memory move with you.

## Supported sources and delivery channels

| Sources | Delivery channels |
|---------|-------------------|
| Gmail | Console (terminal preview) |
| Google Calendar | Email (SMTP) |
| Notion tasks | Slack (webhook) |
| Web signals | Notion page/database |
| Custom API / RSS | Telegram bot |

## Quick start

1. **Clone the repo** into your workspace:
   ```bash
   git clone https://github.com/hartmut-ux/ai-chief-of-staff.git
   cd ai-chief-of-staff
   ```
2. **Run the interactive installer:**
   ```bash
   python scripts/install.py
   ```
   On systems where `python` is not available, use `python3 scripts/install.py`.
3. **Fill in `.env`** with your API keys, MCP names, and delivery credentials. Never commit `.env`.
4. **Install MCP servers** for Gmail, Calendar, Notion, and Slack (see `docs/mcp-setup.md`).
5. **Run your first briefing:**
   ```bash
   python -m chief_of_staff run --preview
   ```
   Use `python3 -m chief_of_staff run --preview` if your system does not have `python`.
6. **Set your approval dial** in `config/chief_of_staff.toml` (`draft` → `ask` → `auto`).

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
├── chief_of_staff/               # AI-agnostic Python package
│   ├── connectors/               # Source fetchers (email, calendar, tasks, web, custom)
│   ├── delivery/                 # Delivery channels (console, email, slack, notion, telegram)
│   ├── references/               # Connector schema and briefing template
│   ├── assets/                   # HTML/Jinja2 rendering template
│   ├── __main__.py               # Entry point for `python -m chief_of_staff`
│   ├── cli.py                    # argparse CLI
│   ├── runner.py                 # GATHER → SYNTHESIZE → DELIVER orchestrator
│   ├── synthesis.py              # Merge, rank, and render the briefing
│   ├── memory.py                 # Preferences and feedback management
│   └── config.py                 # Load .env and config/chief_of_staff.toml
├── scripts/                      # Helper scripts
│   ├── install.py                # Interactive setup wizard
│   └── run_briefing.py           # Backward-compatible wrapper
├── .kimi/skills/chief-of-staff/   # Kimi skill definition
├── .claude/skills/chief-of-staff/ # Claude skill definition
├── .codex/skills/chief-of-staff/  # Codex skill definition
├── .github/                      # GitHub Actions workflow
├── memory/                       # Runtime memory, cache, history, output
│   ├── preferences.md
│   ├── source-cache/
│   ├── history/
│   └── output/
└── docs/
    ├── index.md                  # Landing-page copy
    ├── setup.md                  # Step-by-step setup guide
    ├── mcp-setup.md              # Gmail, Calendar, Notion MCP setup
    ├── telegram-setup.md         # Telegram bot setup
    └── architecture.md           # Architecture and data-flow docs
```

## Approval dial

Every action category has an approval level in `config/chief_of_staff.toml`:

- **draft** — generate the message or update, show it to the user, do not send.
- **ask** — show the action and ask for explicit yes/no before executing.
- **auto** — execute without confirmation (use with care).

Default is `draft` for all delivery actions. The dial is per category: email replies, calendar edits, task creation, Slack posts, web publishing, Telegram messages.

## Automation

Run the agent on your laptop or in the cloud:

- **Local cron**: schedule `python -m chief_of_staff run --preview` via your OS cron or a scheduler like `launchd`/`systemd`.
- **GitHub Actions**: use the included workflow (`.github/workflows/daily-briefing.yml`) to run the briefing on a schedule and optionally post to Slack or Notion.

## Sell it / Productize

This project is released under the MIT License. You can:

- Resell it as a template or private setup service.
- Wrap it as a SaaS and charge for hosted orchestration.
- Customize it for executives, investors, or agencies.

The SEO-optimized landing page lives in `docs/index.md` and is published via GitHub Pages.

## Additional resources

- [SEO / AI-search optimized landing page](docs/index.md) — copy for your GitHub Page.
- [Personal Kimi setup guide](docs/setup-kimi-personal.md) — step-by-step setup for your own Mac with Kimi Code CLI.
- [Skill portal strategy](docs/skill-portal-strategy.md) — how to publish your Claude Skills for Kimi, Claude and Codex.
- [Skill portal template](skill-portal/) — reusable template for a multi-platform skill library.

## Roadmap

- **Memory loop** — learn from approvals, rejections, and recurring tasks.
- **Drafted replies** — generate reply drafts for high-priority emails.
- **Time blocking** — propose and optionally write focus blocks into the calendar.
