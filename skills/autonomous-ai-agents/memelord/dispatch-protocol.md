# MemeLord — Dispatch Protocol

Prompt templates passed to `delegate_task(role="leaf", goal=..., context=...)`
whenever Momo needs to delegate meme work to the MemeLord sub-agent.

## Template (3-meme daily digest)

```text
goal: |
  Generate 3 static-image memes for the Discord memes channel.
  Today's buckets: {BUCKET_1}, {BUCKET_2}, {BUCKET_3}.
  Buckets are drawn from: tech, design, investment, product management, AI.
  Aim for variety — do not use the same bucket twice in one digest.

context: |
  Style: Discord-friendly, dark humor OK, no slurs, no NSFW, no doxxing.
  Format for each meme (3 of them, in this order):

    **Meme 1 — <bucket>**
    MEDIA:/absolute/path/to/image.png
    <one-line caption, optional>

  Forbidden:
    - GIFs and videos (image_generate returns static PNGs).
    - Text-only jokes.
    - More than 3 memes, fewer than 3 memes.

  Delivery:
    - Return the 3 meme blocks in your final assistant message.
    - Do NOT call discord tools to post — the orchestrator forwards.
    - The image_generate tool returns a local path. Use that exact path
      in the MEDIA: line.

  End with the literal line:
    "React 👍 or 👎 to each — tell me what to lean into or drop and I'll update the meme preferences."

  Skills to load: image_generate (built-in), gif-search (fallback only).
```

## Template (single ad-hoc meme, e.g. user asks "send me a meme about X")

```text
goal: |
  Generate 1 static-image meme for the Discord memes channel.
  Topic: {USER_TOPIC}.

context: |
  Same style and constraints as the 3-meme digest, but only 1 meme.
  One-line caption is required (not optional) for ad-hoc requests.
  No "react 👍/👎" footer — that's a digest-only call-to-action.
```

## Template (GIF reaction)

```text
goal: |
  Find ONE reaction GIF for the Discord memes channel.
  Tone: {TONE — e.g. "approval", "lol", "this is fine", "thumbs up"}.

context: |
  Use the gif-search skill (Tenor API). Pick the most fitting GIF.
  Return as: MEDIA:/absolute/path/to/file.gif (download via curl first).
  No captions needed.
```

## Variable reference

| Variable       | Example                              | Notes                                    |
|----------------|--------------------------------------|------------------------------------------|
| `{BUCKET_*}`   | `tech`, `AI`, `product management`   | Pick from the 5-bucket rotation list     |
| `{USER_TOPIC}` | User's free-form meme request        | Pass through verbatim                    |
| `{TONE}`       | `approval`, `lol`, `this is fine`    | Single short phrase for Tenor search     |

## Verification

After the sub-agent returns:
1. Momo (orchestrator) checks that each line starting with `MEDIA:` points
   to a real local file (`stat /path` succeeds).
2. Momo forwards the formatted output to the memes channel via the standard
   delivery path.
3. For scheduled cron deliveries, the cron job's `deliver` field handles
   channel routing automatically.
