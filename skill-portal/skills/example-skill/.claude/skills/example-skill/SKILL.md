---
name: example-skill
description: Example multi-platform skill for Claude Code. Demonstrates the shared-core + thin-wrapper pattern.
---

# Example Skill — Claude wrapper

This is the **Claude Code wrapper** for `example-skill`. The full skill definition lives in `shared/SKILL-CORE.md` in the same skill folder.

## When to use

Use when the user asks for:
- `example-skill`
- "/skill:example-skill"
- "run the example skill"

## How to invoke

In Claude Code:

```
example-skill
```

## Instructions

1. Read `shared/SKILL-CORE.md` for the platform-agnostic workflow and rules.
2. Execute the workflow using Claude Code tools.
3. Keep responses concise and reference the shared core pattern.

## References

- `shared/SKILL-CORE.md` — full skill definition
