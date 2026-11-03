# Agents Context

## Project Overview
Public-facing portfolio showcasing the Hermes Agent system. Not a working codebase — a reference doc for other Hermes users.

## What This Repo Is
- README.md — high-level overview for visitors
- SKILLS.md — generated inventory of installed shared skills; counts must be regenerated from disk
- docs/architecture.md — technical architecture (sub-agent layer included)
- skills/ — skill examples and templates

## Important
- **Do not commit private info**: API keys, tokens, phone numbers, internal file paths, config contents
- **Do not include real cron job IDs** in public docs
- This is a static reference — no code to run, no tests to pass

## Conventions for Updates
- Skills count and category counts must match current state
- Update review dates to the actual month and year; do not leave stale fixed-date instructions
- Cron job schedules can be described generically (e.g., "daily at 7am IST") without exposing internal IDs
- Platform names: Discord, Telegram, Photon (iMessage) — don't expose channel IDs
- **Specialist section**: when adding/removing a `delegate_task` agent or a profile-based specialist, update README.md, docs/architecture.md, the config reference, and SKILLS.md when the shared installed-skill inventory changes. Keep dispatch routing explicit: not every specialist uses `delegate_task`.
- Keep runtime facts source-backed. Record provider/model defaults separately from profile, cron, and auxiliary overrides; never claim every job/profile uses the default unless verified.

## Branch
- Default: `master`