# Sample Skill Template

This is a template for creating new skills in the Hermes Agent system.

## Structure

```
skills/
└── category/
    └── skill-name/
        ├── SKILL.md           # Required: Main skill definition
        ├── references/        # Optional: Supporting docs
        ├── templates/         # Optional: Config templates
        └── scripts/          # Optional: Helper scripts
```

## SKILL.md Format

```yaml
---
name: skill-name
description: Brief description of what this skill does
category: category-name
toolsets:
  - terminal
  - file
tags:
  - example
  - template
version: 1.0.0
---

# Skill Name

Brief description of the skill.

## When to Use

Use this skill when [specific use case].

## Requirements

- Requirement 1
- Requirement 2

## Usage

```bash
# Example command
some-command --example
```

## Notes

Any additional notes or caveats.
```

## Example Skill

See `skills/examples/stock-screener/` for a complete example.

## Categories

Available categories:
- autonomous-ai-agents
- creative
- data-science
- email
- financial-analysis
- github
- media
- mlops
- note-taking
- productivity
- red-teaming
- research
- smart-home
- social-media
- software-development

## Toolsets

Available toolsets:
- terminal (shell commands)
- file (file operations)
- web (web search)
- browser (browser automation)
- code_exec (Python execution)
- delegation (subagent spawning)
- cronjob (scheduled tasks)
- skills (skill management)
- mcp (MCP tools)

---

*Template version: 1.0.0*