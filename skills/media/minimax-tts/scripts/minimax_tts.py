#!/usr/bin/env python3
"""MiniMax TTS helper.

Calls the MiniMax Speech 2.8 endpoint directly and writes an MP3 to disk.
Bypasses Hermes' built-in TTS providers (which don't include minimax yet).

Auth: reuses the same MINIMAX_API_KEY Hermes already loads internally.
We pull it via `hermes auth list --reveal` so the user doesn't have to
duplicate the secret.

Usage:
    python minimax_tts.py "Hello world" --voice English_PassionateWarrior \
        --out /tmp/out.mp3

Returns the absolute output path on stdout, non-zero on error.
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error

MINIMAX_TTS_URL = "https://api.minimax.io/v1/t2a_v2"
DEFAULT_VOICE = "English_PassionateWarrior"
DEFAULT_MODEL = "speech-2.8-hd"

# Common MiniMax TTS voices (from platform docs)
VOICES = [
    "English_PassionateWarrior",
    "English_Graceful_Lady",
    "English_Trustworth_Man",
    "English_Comedian",
    "English_Sentimental_Man",
    "English_Insightful_Speacker",
    "English_Generous_Leader",
    "English_Reserved_Youth",
    "English_Playful_Spirit",
    "English_Passionate_Woman",
]


def get_api_key() -> str:
    """Pull MINIMAX_API_KEY from one of these sources (in order):
    1. ~/.hermes/auth/minimax_tts.token (recommended; chmod 600)
    2. MINIMAX_API_KEY env var
    """
    # Preferred: dedicated token file (set via `hermes auth add` or written directly)
    token_path = os.path.expanduser("~/.hermes/auth/minimax_tts.token")
    if os.path.exists(token_path):
        with open(token_path) as f:
            key = f.read().strip()
        if key:
            return key

    # Fallback: env var (works if user has set it in their shell rc)
    env_key = os.environ.get("MINIMAX_API_KEY")
    if env_key:
        return env_key.strip()

    print("ERROR: MINIMAX_API_KEY not found.", file=sys.stderr)
    print("", file=sys.stderr)
    print("Create the token file:", file=sys.stderr)
    print("  mkdir -p ~/.hermes/auth", file=sys.stderr)
    print("  chmod 600 ~/.hermes/auth/minimax_tts.token", file=sys.stderr)
    print("  echo 'your-minimax-api-key' > ~/.hermes/auth/minimax_tts.token",
          file=sys.stderr)
    print("", file=sys.stderr)
    print("Or set MINIMAX_API_KEY in your shell environment.", file=sys.stderr)
    sys.exit(2)


def synthesize(text: str, voice: str, model: str, api_key: str, out_path: str) -> str:
    payload = {
        "model": model,
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice,
            "speed": 1.0,
            "vol": 1.0,
            "pitch": 0,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1,
        },
        "language_boost": "auto",
    }

    req = urllib.request.Request(
        MINIMAX_TTS_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Hermes-minimax-tts/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read()
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")[:500]
        print(f"ERROR: MiniMax TTS HTTP {exc.code}: {err_body}", file=sys.stderr)
        sys.exit(3)
    except urllib.error.URLError as exc:
        print(f"ERROR: MiniMax TTS connection failed: {exc}", file=sys.stderr)
        sys.exit(3)

    # MiniMax T2A v2 returns JSON with hex-encoded audio under data.audio
    try:
        decoded = json.loads(body)
    except json.JSONDecodeError:
        print(f"ERROR: response is not JSON", file=sys.stderr)
        sys.exit(3)

    base_resp = decoded.get("base_resp", {})
    if base_resp.get("status_code", 0) != 0:
        err_msg = base_resp.get("status_msg", "unknown error")
        print(f"ERROR: MiniMax API: {err_msg}", file=sys.stderr)
        sys.exit(3)

    data = decoded.get("data") or {}
    audio_hex = data.get("audio", "")
    if not audio_hex:
        print(f"ERROR: no audio in response. keys: {list(decoded.keys())}",
              file=sys.stderr)
        sys.exit(3)

    # Hex-decode to raw MP3 bytes
    try:
        audio_bytes = bytes.fromhex(audio_hex)
    except ValueError as exc:
        print(f"ERROR: audio is not hex: {exc}", file=sys.stderr)
        sys.exit(3)

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(audio_bytes)

    return out_path


def main():
    parser = argparse.ArgumentParser(description="MiniMax Speech 2.8 TTS")
    parser.add_argument("--list-voices", action="store_true",
                        help="List available voices and exit")
    parser.add_argument("--voice", default=DEFAULT_VOICE,
                        choices=VOICES, help=f"Voice (default: {DEFAULT_VOICE})")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        choices=["speech-2.8-hd", "speech-2.8-turbo",
                                 "speech-02-hd", "speech-02-turbo"],
                        help=f"Model (default: {DEFAULT_MODEL})")
    parser.add_argument("--out", default="/tmp/minimax_tts_out.mp3",
                        help="Output path (default: /tmp/minimax_tts_out.mp3)")
    parser.add_argument("text", nargs="?", default=None,
                        help="Text to synthesize")
    args = parser.parse_args()

    if args.list_voices:
        print("\n".join(VOICES))
        return

    api_key = get_api_key()
    out = synthesize(args.text, args.voice, args.model, api_key, args.out)
    print(out)


if __name__ == "__main__":
    main()