---
title: "AI Chief of Staff — Daily Briefing for Kimi, Claude & Codex"
description: "Free, open-source AI chief of staff that reads your inbox, calendar, tasks and web signals, then delivers one prioritized daily briefing with actions you can approve in one click. Works with Kimi Code CLI, Claude Code and Codex CLI."
keywords:
  - AI chief of staff
  - daily briefing automation
  - personal AI assistant
  - Kimi Code CLI skill
  - Claude Code skill
  - Codex CLI skill
  - inbox calendar task automation
  - founder productivity tool
  - AI executive assistant
  - no-code AI automation
---

# AI Chief of Staff — Your Daily Briefing, Built for Kimi, Claude & Codex

**Start your day knowing exactly what matters.**

This open-source AI chief of staff connects to your **Gmail, Google Calendar, Notion tasks, Slack, Telegram and web signals**, then creates one short, prioritized briefing every morning. It tells you what deserves your attention and drafts the actions you can approve with one click.

It runs inside **Kimi Code CLI**, **Claude Code** or **Codex CLI** — so you keep your assistant, your data, and your workflow.

[Get the GitHub repo](https://github.com/hartmut-ux/ai-chief-of-staff) · [Setup guide](setup.md) · [Kimi setup for your Mac](setup-kimi-personal.md) · [MCP setup](mcp-setup.md)

---

## What is an AI chief of staff?

An AI chief of staff is like a highly efficient executive assistant that lives inside your AI assistant. Every day it:

- Reads your inbox and flags the emails that need a decision.
- Checks your calendar for conflicts and prep needs.
- Pulls your open tasks from Notion or other tools.
- Scans the web for news, competitors and relevant signals.
- Delivers one concise briefing with suggested actions.

Instead of opening ten apps, you get one summary and a short list of "approve or skip" actions.

---

## What this project does

The AI Chief of Staff is a **personal automation engine** that turns scattered information into a single, prioritized daily briefing:

- **Email** — surfaces high-intent messages, deal risks and requested actions.
- **Calendar** — flags conflicts, prep needs and focus-time violations.
- **Tasks** — pulls outstanding todos from Notion, Todoist or Asana.
- **Web signals** — tracks competitors, news and industry updates.
- **Custom sources** — connects any API, RSS feed or database.

It then synthesizes everything into a concise markdown briefing and delivers it to your terminal, email, Slack, Notion or Telegram.

```text
GATHER → SYNTHESIZE → DELIVER
sources   daily-briefing.md   console / email / Slack / Notion / Telegram
```

---

## Why use this instead of another app?

| Typical productivity app | AI Chief of Staff |
|---|---|
| Locked into one vendor | Runs on Kimi, Claude **and** Codex |
| Generic notifications | Ranked by **your** priorities: revenue → team → customers → deep work |
| Forces new UI habits | Lives inside your existing AI assistant |
| Sends without asking | Approval dial: **draft**, **ask** or **auto** per category |
| Closed source, monthly fee | MIT licensed — run locally, modify, resell |

---

## How it works — step by step

1. **Connect your sources**  
   Link Gmail, Google Calendar, Notion, Slack, Telegram or any custom API/RSS feed via MCP servers.

2. **Set your priorities**  
   Edit `constitution.md` and `memory/preferences.md` so the chief of staff learns what matters to you.

3. **Choose the approval dial**  
   Pick `draft` (show only), `ask` (prompt before sending) or `auto` (execute) per action category. Defaults are safe.

4. **Run your briefing**  
   - In Kimi: `/chief-of-staff`
   - In Claude or Codex: `chief-of-staff`
   - From the terminal: `python -m chief_of_staff run --preview`

5. **Review and approve actions**  
   Read the briefing, confirm proposed replies, calendar updates or Slack posts, and let the engine execute them.

6. **Schedule it**  
   Run locally via cron/`launchd`/`systemd`, or use the included GitHub Actions workflow for cloud delivery.

---

## Who this is for

- **Founders and operators** who want to protect deep-work time and never miss a revenue risk.
- **Executives** who receive hundreds of emails and need a filter before the workday starts.
- **Agencies and consultants** who want to productize a daily-briefing service for clients.
- **AI power users** who switch between Kimi, Claude and Codex and want one reusable workflow.
- **Busy professionals** who are tired of tab-switching and want one place to start the day.

---

## Supported AI frontends

| Assistant | How to invoke | Skill location |
|---|---|---|
| **Kimi Code CLI** | `/chief-of-staff` | `.kimi/skills/chief-of-staff/SKILL.md` |
| **Claude Code** | `chief-of-staff` | `.claude/skills/chief-of-staff/SKILL.md` |
| **Codex CLI** | `chief-of-staff` | `.codex/skills/chief-of-staff/SKILL.md` |

One engine powers all three frontends, so your configuration and memory move with you.

---

## Supported sources and delivery channels

| Sources | Delivery channels |
|---|---|
| Gmail | Console (terminal preview) |
| Google Calendar | Email (SMTP) |
| Notion tasks | Slack (webhook) |
| Web signals | Notion page or database |
| Custom API / RSS | Telegram bot |
| Slack / Telegram | — |

---

## Quick start

```bash
git clone https://github.com/hartmut-ux/ai-chief-of-staff.git
cd ai-chief-of-staff
python3 scripts/install.py
# fill in .env, register MCP servers, then:
python3 -m chief_of_staff run --preview
```

See the [full setup guide](setup.md) or the [personal Kimi setup for your Mac](setup-kimi-personal.md).

---

## Frequently asked questions

### What is an AI chief of staff?
An AI chief of staff is a software agent that collects information from your inbox, calendar, task manager and news sources, then produces a short, prioritized daily briefing with suggested actions.

### Does this work with Kimi Code CLI?
Yes. The project includes a Kimi skill wrapper at `.kimi/skills/chief-of-staff/SKILL.md`. After setup, invoke it with `/chief-of-staff`.

### Can I use the same setup with Claude Code or Codex?
Yes. The engine is AI-agnostic. Thin skill wrappers for Claude and Codex teach each assistant how to invoke the same engine.

### Is my data sent to third parties?
No. The engine runs locally on your machine. Only the MCP servers and APIs you configure (Gmail, Notion, Slack, etc.) are contacted, using your own credentials.

### How does the approval dial work?
Every action category has an approval level in `config/chief_of_staff.toml`: `draft` shows the output without sending, `ask` prompts you before execution, and `auto` executes without confirmation. Defaults are set to `draft` for safety.

### Can I schedule the briefing automatically?
Yes. You can schedule it locally with cron or `launchd`, or enable the included GitHub Actions workflow for cloud-based scheduled runs.

### Do I need to code?
No. The interactive installer sets up the configuration for you. You only need to copy your API keys and MCP names into `.env`.

### What license is this under?
MIT. You can run it yourself, customize it, resell it as a template, or wrap it into a SaaS.

---

## Productize it

This project is released under the MIT License. You can:

- Resell it as a private setup service.
- Wrap it as a SaaS and charge for hosted orchestration.
- Customize it for executives, investors or agencies.

---

*Open source under MIT. Run it locally, schedule it in the cloud, or productize it for your clients.*
