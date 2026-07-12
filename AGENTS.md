# Agents Context

## Project Overview
Public-facing portfolio showcasing the Hermes Agent system. Not a working codebase — a reference doc for other Hermes users.

## What This Repo Is
- README.md — high-level overview for visitors
- SKILLS.md — full inventory of 85 skills across 20 categories
- docs/architecture.md — technical architecture
- skills/ — skill examples and templates

## Important
- **Do not commit private info**: API keys, tokens, phone numbers, internal file paths, config contents
- **Do not include real cron job IDs** in public docs
- This is a static reference — no code to run, no tests to pass

## Conventions for Updates
- Skills count and category counts must match current state
- All timestamps in documentation should use "June 2026"
- Cron job schedules can be described generically (e.g., "daily at 7am IST") without exposing internal IDs
- Platform names: Discord, Telegram, Photon (iMessage) — don't expose channel IDs

## Branch
- Default: `master`
