# Example Skill — Core Definition

This file contains the platform-agnostic definition of the skill. It is referenced by the thin wrappers for Kimi, Claude and Codex.

## Purpose

Use this skill when the user asks for an example workflow or template demonstration.

## Trigger phrases

- "run the example skill"
- "show me the example workflow"
- "example skill"

## Workflow

1. Greet the user and confirm the request.
2. Explain the shared-core + thin-wrapper pattern.
3. Offer to create a new skill based on this template.

## Rules

- Keep responses concise.
- Reference `shared/SKILL-CORE.md` as the single source of truth.
- Do not duplicate core logic in platform wrappers.

## Output format

```text
Example Skill Output
====================
1. Shared core: shared/SKILL-CORE.md
2. Kimi wrapper:  .kimi/skills/example-skill/SKILL.md
3. Claude wrapper: .claude/skills/example-skill/SKILL.md
4. Codex wrapper:  .codex/skills/example-skill/SKILL.md
```

## References

- [Multi-platform skill strategy](../../../docs/skill-portal-strategy.md)
- [Portal README](../../../README.md)
