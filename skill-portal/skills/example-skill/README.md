# example-skill

A template multi-platform AI skill. Use this folder as a starting point for your own skills.

## Structure

```text
example-skill/
├── README.md
├── shared/
│   └── SKILL-CORE.md          # Platform-agnostic skill definition
├── .kimi/skills/example-skill/
│   └── SKILL.md               # Kimi wrapper
├── .claude/skills/example-skill/
│   └── SKILL.md               # Claude wrapper
└── .codex/skills/example-skill/
    └── SKILL.md               # Codex wrapper
```

## Packaging

From the repository root:

```bash
python scripts/package-skill.py example-skill
```

This produces:

- `dist/example-skill-all.zip`
- `dist/example-skill-kimi.zip`
- `dist/example-skill-claude.zip`
- `dist/example-skill-codex.zip`
