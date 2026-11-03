# Hermes Agent Configuration Template

This is an illustrative reference for a Hermes setup, reviewed November 2026. It is Markdown documentation, not a drop-in `config.yaml`: the inline `subagents` and `profiles` examples below describe routing conventions and are not native Hermes configuration schemas. Use `hermes config` and `hermes profile` for actual runtime configuration.

## Usage

```bash
# This Markdown reference is not a valid config.yaml. Start with `hermes setup`.
hermes setup
```

## Model Configuration

The live setup uses **Nous** with `openai/gpt-6-luna` as the default model for Momo and delegation. Profile and cron overrides exist; not every scheduled job uses the default. Three enabled LLM crons currently pin `z-ai/glm-5.3-flash`, while script-only jobs have no model.

```yaml
model:
  default: openai/gpt-6-luna
  provider: nous
  # Current auxiliary vision, web extraction, and compression route:
  # provider: nous; model: meituan/longcat-2.5-preview:free
delegation:
  model: openai/gpt-6-luna
  provider: nous
  max_concurrent_children: 5
```

### Provider Notes
- **Nous** — primary provider; default model `openai/gpt-6-luna`, auxiliary model `meituan/longcat-2.5-preview:free`
- **Per-job and per-profile model overrides** — pin only where required; script-only cron jobs do not invoke an LLM
- **Claude Code / Codex / OpenCode CLIs** — separate coding-agent execution (never writes code inline in Hermes)

## Tool Sets

```yaml
toolsets:
  - terminal      # Shell commands
  - file          # File operations
  - web           # Web search
  - browser       # Browser automation
  - code_exec     # Python execution
  - delegation    # Sub-agent dispatch (delegate_task)
```

Tool names in this illustrative list are descriptive; check the live Hermes tool registry before copying any configuration.

## Memory

Two-tier memory. Hermes memory is the always-on budget (~2,200 chars); OpenViking is the long-term semantic store (unlimited, at 127.0.0.1:1933).

```yaml
memory:
  hermes:
    enabled: true
    budget_chars: 2200
  openviking:
    enabled: true
    endpoint: http://localhost:1933
```

## Specialist Routing (illustrative pseudo-config)

Momo is the orchestrator. Ten specialists are dispatched through `delegate_task`. A separate wildlife-photo caption specialist runs in the `wildlifephoto` profile via a local helper; it receives image observations and actually extracted EXIF, returns drafts only, and never publishes. These are routing examples, not keys understood by Hermes config parsing:

```yaml
subagents:
  macpilot:      { profile: macpilot,      skills: [computer-use, tailscale-mac-remote-access] }
  stockman:      { skills: [stockman, stock-prediction-model] }
  taxbuddy:      { profile: tax-assist,    skills: [india-rsu-tax-filing] }
  homebase:      { profile: homebase,      skills: [] }      # private case data stays out of this repo
  healthguard:   { profile: healthguard,   skills: [ultrahuman-insights] }
  familydoc:     { profile: familydoc,     skills: [familydoc, pregnancy-milestone-tracker] }
  codeforge:     { profile: codeforge,     skills: [github-pr-workflow] }
  researcher:    { profile: researcher,    skills: [linkup-research, arxiv, blogwatcher] }
  qabot:         { profile: qabot,         skills: [dogfood, github-pr-workflow] }
  hsbcmm:        { profile: hsbc-credit-card-manager, skills: [hsbc-credit-card-manager] }
  wildlifephoto: { profile: wildlifephoto, route: dedicated-caption-helper, publishes: false }
```

The `delegate_task` dispatch contract lives in the `agent-orchestration` skill; personalities in `sub-agent-personalities`; hard rules in `sub-agent-guardrails`. Each gets a goal + context and returns a short summary. The wildlife-caption helper is deliberately separate from `delegate_task` and has a draft-only contract.

## Profiles (illustrative inventory)

Persistent contexts carrying their own memory, skills, and config across sessions. Specialist profiles are visible in the Hermes desktop **Bots** tab:

```yaml
profiles:
  default:          { description: Main Momo profile (orchestrator) }
  stockman:         { description: Equity research + daily prediction }
  homebase:         { description: Property + loan + watchdog }
  healthguard:      { description: Insurance + health trends }
  familydoc:        { description: Family physician triage }
  codeforge:        { description: Side-project scoping → Claude Code handoff }
  researcher:       { description: Multi-source deep dives }
  qabot:            { description: QA after builds }
  macpilot:         { description: Mac automation over Tailscale }
  tax-assist:       { description: Sustained ITR work; TaxBuddy's profile }
  hsbc-credit-card-manager: { description: Credit card statement analysis }
  wildlifephoto:            { description: Dedicated wildlife-photo caption specialist; never publishes }
```

## Cron Jobs (illustrative only)

Hermes cron runs scheduled jobs; the live schedule is maintained in the user's private configuration and changes over time. These entries illustrate the shape only, not a full or current importable fleet. Reference: https://hermes-agent.nousresearch.com/docs

```yaml
cron:
  default_delivery: discord     # scheduled delivery routed to the user's active home channel
  jobs:
    - name: Unified Morning Digest
      schedule: "15 8 * * *"   # 8:15am IST; representative current workflow
      skills: [arxiv, blogwatcher]
    - name: Daily WMT Stock Price
      schedule: "30 0 * * 1-5"  # 6am IST Mon–Fri
    - name: Ultrahuman sync + insights
      schedule: "30 6 * * *"
      script: sync_then_insights.py
      no_agent: true
    - name: Daily Morning Prediction
      schedule: "0 9 * * 1-5"   # 9am IST Mon–Fri
      skills: [stock-prediction-model, stockman]
    - name: MailScout expense digest
      schedule: "30 14 * * *"   # 2:30pm IST
      skills: [himalaya]
    - name: HomeBase Watchdog
      schedule: "0 10 * * *"    # 10am IST
      skills: [agent-orchestration]
```

Notes:
- **No `delegate_task` inside cron** — each cron prompt is a thin self-contained orchestrator; the cron session cannot spawn leaf sub-agents.
- Script-only jobs (`no_agent: true`) deliver script stdout; return 0 so a useful message survives a "failed" run.
- All scheduled/reminder text is **English only** (no Hinglish in cron output).

## MCP + Ops Integrations (illustrative)

```yaml
mcp:
  kite:          { enabled: true }   # Zerodha Kite — auth is in-memory; prediction crons prefer yfinance fallback
  github:        { enabled: true }
  ibkr:          { enabled: true }   # via Claude Code CLI + IBKR MCP
  discord:       { enabled: true }
  discord_admin: { enabled: true }
  openhue:       { enabled: true }   # Philips Hue
  apple_reminders: { enabled: true } # via remindctl on the Mac

# External ops (not MCP):
ops:
  whatsapp:      { wa_bridge: "ws://<vps>:8765" }   # VPS wa-bridge read/send
  location:      { owntracks: { broker: "mosquitto+TLS", enabled: true } }
  mac:           { macpilot: { tailscale: "<mac>.ts.net", enabled: true } }
```

## Platform Integration

```yaml
telegram:
  bot_token: YOUR_TELEGRAM_BOT_TOKEN
  allowed_chats: [YOUR_CHAT_ID]

discord:
  bot_token: YOUR_DISCORD_BOT_TOKEN
  server_id: YOUR_SERVER_ID
  channel_prompts: {}

photon:                           # iMessage via Photon
  enabled: true

whatsapp:                         # VPS wa-bridge (separate from Mac WhatsApp Web)
  wa_bridge_url: "ws://<vps>:8765"
```

## Delivery Routing

The live setup routes scheduled deliveries intended for Telegram to Discord.

```yaml
delivery:
  fallbacks:
    - platform: telegram
      route_to: discord
      channel: "#general"
```

## Security Reminders

- Never commit this file with real API keys
- Use environment variables or Hermes auth flows for secrets; never hard-code credentials
- macOS credentials (VNC etc.) are passed via env vars at runtime only, never persisted to disk
- Hermes respects `.env` files at the workspace root
- Keep credentials private and least-privilege; do not commit profile secrets

---

*Reference last reviewed November 2026*