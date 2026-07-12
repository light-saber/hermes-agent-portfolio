---
name: minimax-tts
description: Text-to-speech via MiniMax Speech 2.8 HD endpoint. Use when you need high-quality English narration through the MiniMax platform (Bundled with the MiniMax Token Plan Subscription). Bypasses the Hermes built-in TTS providers (which do not include MiniMax). Outputs MP3 or OGG/Opus for Discord/Telegram voice messages.
category: media
toolsets:
  - terminal
tags:
  - tts
  - speech
  - audio
  - minimax
  - minimax-speech-2.8
version: 1.0.0
---

# MiniMax TTS

Text-to-speech using the MiniMax Speech 2.8 HD endpoint directly. Useful
when you have a MiniMax Token Plan Subscription that includes speech
quota but the Hermes built-in `text_to_speech` tool does not yet list
MiniMax as a provider.

## Why this skill exists

Hermes Agent ships with several TTS providers (edge, openai, gemini,
xai, mistral, elevenlabs, neutts, piper) but does not currently include
MiniMax. If your subscription includes MiniMax Speech 2.8, this skill
gives you a direct path to that endpoint.

## Quick start

```bash
# 1. Save your API key (one-time)
mkdir -p ~/.hermes/auth
echo "sk-cp-..." > ~/.hermes/auth/minimax_tts.token
chmod 600 ~/.hermes/auth/minimax_tts.token

# 2. Synthesize speech
python ~/.hermes/scripts/minimax_tts.py \
  "Hello from MiniMax Speech 2.8 HD" \
  --voice English_PassionateWarrior \
  --out /tmp/out.mp3
```

## Voices

Run `python minimax_tts.py --list-voices` for the full list. Common
choices:

- `English_PassionateWarrior` — male, energetic (good for news/weather)
- `English_Generous_Leader` — male, authoritative
- `English_Graceful_Lady` — female, polished
- `English_Comedian` — male, expressive

## Discord / Telegram delivery

Discord desktop can be finicky about Opus voice messages sent as MEDIA
references — sometimes it shows the file but won't auto-play. If that
happens, convert to OGG/Opus at 48 kHz and use the
`voice-message.ogg` filename (Hermes's voice-message delivery path):

```bash
ffmpeg -i out.mp3 -c:a libopus -b:a 64k -application voip \
  -ar 48000 -ac 1 -map_metadata -1 voice-message.ogg
```

## Models

- `speech-2.8-hd` (default, highest quality)
- `speech-2.8-turbo` (faster, lower cost)
- `speech-02-hd` / `speech-02-turbo` (older tier)

## Auth

The script reads the API key from one of these sources (in order):

1. `~/.hermes/auth/minimax_tts.token` (recommended; chmod 600)
2. `MINIMAX_API_KEY` environment variable

It does not reuse the encrypted credential pool that the Hermes
gateway uses for text generation — direct API calls need a plaintext
token. Store it like any other API secret.