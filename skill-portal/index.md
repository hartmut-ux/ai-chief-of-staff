---
title: "AI Skills for Kimi, Claude & Codex"
description: "Download AI skills that run on Kimi Code CLI, Claude Code and Codex CLI. One shared core, thin per-platform wrappers."
keywords:
  - Kimi Code CLI skills
  - Claude Code skills
  - Codex CLI skills
  - AI skill library
  - multi-platform AI skills
---

# AI Skills for Kimi, Claude & Codex

A library of reusable AI skills that work across **Kimi Code CLI**, **Claude Code**, and **Codex CLI**. Each skill is maintained once and packaged automatically for every assistant.

## Why multi-platform skills matter

Most skills are tied to one assistant. This portal uses a **shared core + thin wrapper** pattern so you can:

- Write a skill once and ship it everywhere.
- Let users pick their favorite AI assistant.
- Keep maintenance low as assistants evolve.

## How to install a skill

### Kimi Code CLI

```bash
# Download the -kimi.zip or -all.zip, extract it, then:
cp -R .kimi/skills/<skill-name> ~/.kimi/skills/
```

Invoke in Kimi with `/<skill-name>`.

### Claude Code

```bash
# Download the -claude.zip or -all.zip, extract it, then:
cp -R .claude/skills/<skill-name> ~/.claude/skills/
```

Invoke in Claude with `<skill-name>`.

### Codex CLI

```bash
# Download the -codex.zip or -all.zip, extract it, then:
cp -R .codex/skills/<skill-name> ~/.codex/skills/
```

Invoke in Codex with `<skill-name>`.

## Available skills

| Skill | Description | Download |
|---|---|---|
| [example-skill](skills/example-skill/) | Template skill showing the multi-platform structure. | [all](releases/download/latest/example-skill-all.zip) · [kimi](releases/download/latest/example-skill-kimi.zip) · [claude](releases/download/latest/example-skill-claude.zip) · [codex](releases/download/latest/example-skill-codex.zip) |

## For skill authors

Want to add your own skill? See the [README](README.md) and copy `skills/example-skill/` as a starting point.

---

*Open source under MIT.*
