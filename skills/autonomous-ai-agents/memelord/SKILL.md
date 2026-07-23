---
name: memelord
description: Delegate Discord meme work to a MemeLord sub-agent — image generation, GIF search, captions, daily digest
category: autonomous-ai-agents
toolsets:
  - terminal
  - file
tags:
  - memes
  - discord
  - image-generation
  - gif-search
  - sub-agent
  - dispatch
version: 1.0.0
author: Momo (Hermes Agent)
license: MIT
---

# MemeLord — Discord Meme Sub-Agent

A specialist sub-agent that handles all meme-related work for a Discord
channel so the orchestrator (Momo) does not have to spend its own context
on image generation, GIF search, captioning, or daily meme curation.

## What it does

| Task | Tool used inside the sub-agent |
|------|-------------------------------|
| Generate static image memes | `image_generate` (OpenAI gpt-image-2-medium) |
| Search/download reaction GIFs | `gif-search` skill (Tenor API) |
| Write captions / one-liners | LLM (leaf role) |
| Curate daily meme digest | Cron-driven, 3 buckets / day, no repeats |

## When to dispatch

Dispatch to MemeLord instead of calling `image_generate` directly when:

- The user asks for a meme, GIF, or reaction image for a Discord channel.
- The user wants to "react to" a post with a meme or GIF.
- A daily digest of memes is needed for a specific channel.

Inline (no dispatch) when a single tool call suffices — e.g. "render this
prompt as an image" for a one-off artifact not destined for a chat.

## Dispatch pattern

```python
delegate_task(
    role="leaf",
    goal=(
        "Generate 3 static-image memes for the Discord memes channel. "
        "Buckets today: tech, design, AI. Static images only — no GIFs. "
        "Use image_generate; return MEDIA:/absolute/path for each."
    ),
    context=(
        "Style: Discord-friendly, dark humor OK, no slurs/NSFW. "
        "Format per meme: **Meme N — <bucket>**\\nMEDIA:/path/to/file\\n<one-line caption>. "
        "End with: 'React 👍 or 👎 to each — tell me what to lean into or drop.'"
    ),
)
```

## Hard constraints

- **Static images only** by default. GIFs are a fallback for quick reactions.
- **No slurs, no NSFW, no doxxing**. Dark humor is fine.
- **3 memes per digest** (not 2, not 5). Bucket rotation: do not repeat the
  same bucket 2 days in a row.
- **Never post text-only jokes** — every meme must include an actual image.
- **Verify URLs before posting** — broken links are worse than no post.

## Cron integration

The `Daily memes` cron (runs daily at 8:30am IST) is fire-and-forget —
Momo's prompt runs directly, calls `image_generate`, and delivers to the
memes channel. Leaf sub-agents cannot be spawned by cron jobs, so this
skill is for **ad-hoc, in-session** meme requests, not cron deliveries.

## Files

- `SKILL.md` — this file
- `dispatch-protocol.md` — prompt templates the orchestrator uses to call
  MemeLord (swap bucket list, channel reference, optional style override)

## Notes

- See the `sub-agent-dispatch` skill for the general delegate_task playbook.
- See `docs/architecture.md` for MemeLord's place in the sub-agent roster.
