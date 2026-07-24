# AI Chief of Staff

A persistent sparring-partner skill for CEOs — the take-away skill from the **Working Systems Live** workshop (Open Innovation with AI, EDIH.li). It keeps working after the workshop day: five modes plus a weekly rhythm, grounded in the *Oxford Handbook of Open Innovation* and the CEO-Guide «Kommunikation neu gedacht 2026».

## What the skill does

| Mode | What you get |
|---|---|
| **Sparring — Open Strategy & Open Innovation** | Structured challenge of your strategic case: knowledge-flow diagnosis (inbound / outbound / coupled), maturity check, options outside your usual search space, NIH/IKEA counter-check, one dated next step |
| **Research kick-off** | A clean deep-research brief you can paste into any research tool: question, scope, source standard (2025/2026), visible uncertainty, success criterion |
| **Idea generator** | Structured divergence (8–12 ideas across categories), then convergence scored on effort / impact / fit, origin-blind — every idea carries a rough benefit estimate (hours saved per month × hourly rate or CHF), the recommended one gets one metric and a 30-day check |
| **Format supplier** | Picks and scripts the right working format: Case Clinic, Future Press Release (+ Press Conference), consent decision, Dialogue Walk, Check-in/Check-out, **Team-Cascade** — including a ready-to-send invitation text |
| **Listening mode** | Active listening, NVC stance. No advice, no frameworks — mirroring and clarifying questions only |
| **Friday impulse** | One useful idea per week, rotating through Open Innovation with AI, Agentic Engineering, Private Knowledge — with a 30–45 minute experiment plus a rough ROI anchor (hours or CHF, one metric, 30-day check) for the coming week |

The skill is deliberately non-salesy. EDIH.li follow-up offers appear at most as a neutral pointer («if you want to go deeper…»).

## The skills in this repository

Six skills, each in a fully self-contained `kimi` / `claude` / `codex` variant:

| Skill | What it does |
|---|---|
| **ai-chief-of-staff** | The persistent sparring partner described above — five modes plus weekly rhythm |
| **ai-scanning-sprint** | Sharpens an ecosystem question on the CEO's strategic case and turns it into a deep-research brief |
| **fpr-journalist** | Critical business journalist who stress-tests a Future Press Release for measurability and customer benefit |
| **gfk-gespraechs-sparring** | Rehearses a difficult or postponed conversation — NVC-based (Rosenberg) role-play sparring |
| **sokratischer-fall-interviewer** | Socratic five-question interview that clarifies the CEO's own case (Case Clinic warm-up) |
| **ki-richtlinie-assistent** | Governance-light assistant: guides a CEO in 20–30 minutes to a first one-page AI policy — allowed tools, data no-gos, shadow AI, AI-Act basics in plain language, quarterly review |

**The Cascade Kit idea:** the formats are built to travel one level down. With the Team-Cascade format (90 minutes), the CEO onboards their own leadership team to the workshop formats and installed skills themselves — no external trainer. New skills such as the ki-richtlinie-assistent deliberately end by pointing the CEO to that cascade step.

## Repository layout

```
skills/ai-chief-of-staff/
├── kimi/
│   ├── SKILL.md                  # complete, self-contained (Kimi Work)
│   └── references/
│       ├── open-innovation-kompakt.md
│       └── formate-kompakt.md
├── claude/
│   ├── SKILL.md                  # complete, self-contained (Claude Cowork)
│   └── references/…              # same files, included in this folder
└── codex/
    ├── SKILL.md                  # complete, self-contained (Codex)
    └── references/…              # same files, included in this folder
```

Each environment folder is **fully self-contained**: the `SKILL.md` carries the complete instructions, and its own `references/` subfolder carries the distilled source material. There are no shared folders and no cross-references outside the folder — copying one environment folder is enough. (This layout deliberately avoids the wrapper bug where a thin SKILL.md pointed to a sibling `shared/` directory that never made it into the release ZIP.)

## Installation (no terminal required)

1. Download the ZIP for your environment (`kimi`, `claude`, or `codex`) from the latest release, or copy the matching folder from this repository.
2. Unzip it.
3. Place the folder `ai-chief-of-staff` (the one containing `SKILL.md` and `references/`) into the custom-skills location of your desktop app:
   - **Kimi Work**: use the skills area of the app settings.
   - **Claude Cowork**: use the skills area of your cowork project/settings.
   - **Codex**: use the skills location your Codex setup provides.
4. Enable the skill in the app.

The exact menu paths change between app versions. If you cannot find the skills area, ask inside the app itself (e.g. «Where do I install a custom skill folder?») — the app knows its own current layout.

## Usage

Just talk to it. Examples:

- «Sparring: Wir überlegen, unsere Wartungsverträge neu aufzusetzen — ich sehe nur interne Optionen.»
- «Erstelle mir ein Research-Briefing zu [Thema].»
- «Ich brauche Ideen, wie wir unser Know-how in der Branche sichtbar machen.»
- «Welches Format passt, wenn ein Entscheid seit drei Sitzungen hängt?»
- «Zuhören-Modus: Ich muss mir etwas von der Seele reden.»
- «Freitag-Impuls, bitte.»

You can switch modes at any time («wechsle in den Ideengenerator»).

## Language

Skill content and instructions are in **German** (Swiss spelling, du-form), because the target users are German-speaking CEOs. This README is in English for repository consistency.

## Context and licence

Built for the EDIH.li CEO workshop «Working Systems Live» by Hartmut Hübner (MMIND.ai). Sources: *Oxford Handbook of Open Innovation* (2024); «Kommunikation neu gedacht» (2021) and CEO-Guide 2026 edition. Free to use and share; not for resale.

## Legacy: the original AI Chief of Staff (v0)

This repository started as the home of the AI Chief of Staff briefing product. That code and documentation remain untouched: `chief_of_staff/`, `scripts/`, `config/`, `memory/`, `docs/` (product docs), `AGENTS.md`, `constitution.md`, `pyproject.toml`. The original v0 README now lives at `docs/legacy-readme-v0.md`. The new `skills/` collection is the workshop-grown next generation of the same idea.
