# Multi-Platform AI Skills Portal

A template repository for publishing AI skills that work across **Kimi Code CLI**, **Claude Code**, and **Codex CLI**.

## How it works

Each skill lives in `skills/<skill-name>/` and contains:

- `shared/SKILL-CORE.md` — the platform-agnostic skill definition.
- `.kimi/skills/<skill-name>/SKILL.md` — thin Kimi wrapper.
- `.claude/skills/<skill-name>/SKILL.md` — thin Claude wrapper.
- `.codex/skills/<skill-name>/SKILL.md` — thin Codex wrapper.

You edit the skill once in `shared/SKILL-CORE.md`. The wrappers only add platform-specific invocation hints and frontmatter.

## Add a new skill

1. Copy the `skills/example-skill/` folder and rename it.
2. Replace the content in `shared/SKILL-CORE.md`.
3. Update the frontmatter in each wrapper `SKILL.md`.
4. Run the packaging script:

   ```bash
   python scripts/package-skill.py example-skill
   ```

5. Commit and push. GitHub Actions will attach the ZIP files to your next release automatically.

## Download structure

For each skill the following ZIP files are produced:

- `<skill>-all.zip` — wrappers for Kimi, Claude and Codex.
- `<skill>-kimi.zip` — Kimi wrapper only.
- `<skill>-claude.zip` — Claude wrapper only.
- `<skill>-codex.zip` — Codex wrapper only.

## GitHub Pages

Enable GitHub Pages on the `main` branch and the `index.md` landing page will be rendered automatically.

## License

MIT — reuse, resell or embed into your own tooling.
