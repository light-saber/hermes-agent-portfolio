# Hermes Agent Configuration Template

This is a template configuration. Copy to `config.yaml` (rename to `.yaml`) and customize with your values. It reflects the reference setup as of August 2026.

## Usage

```bash
# Note: this template is .md for readability; rename to .yaml after copying
cp config/templates/config.example.md config/config.yaml
# Edit the file with your API keys and preferences
```

## Model Configuration

Primary model is **DeepSeek V4 Flash** on **Alibaba (DashScope)** — pinned as the daily driver for Momo, all 10 profile/Bot sub-agents, and every cron job.

```yaml
model:
  default: deepseek-v4-flash-0731   # Momo's default model (bare name)
  provider: alibaba                 # DashScope (Qwen token plan)
  # Auxiliary routing (stays on Nous):
  #   image generation  -> ils_nous::gpt-image
  #   vision / web_extract / compression -> tencent/hy3:free
  fallbacks:
    - nous/ox-alpha                  # documented fallback tier
```

### Provider Notes
- **Alibaba / DashScope** — primary daily-driver for the main agent, sub-agents, and cron jobs
- **Nous** — image generation and auxiliary vision/web-extract/compression; previously the ox-alpha inference tier
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

## Sub-agents (chief-of-staff model)

Momo is the orchestrator. Ten specialists, each also a desktop Bot profile:

```yaml
subagents:
  macpilot:      { profile: macpilot,      skills: [computer-use, tailscale-mac-remote-access] }
  stockman:      { skills: [stockman, stock-prediction-model] }
  taxbuddy:      { profile: tax-assist,    skills: [india-rsu-tax-filing] }
  homebase:      { profile: homebase,      skills: [] }      # case files under ~/.hermes/cases/homebase/
  healthguard:   { profile: healthguard,   skills: [ultrahuman-insights] }
  familydoc:     { profile: familydoc,     skills: [familydoc, pregnancy-milestone-tracker] }
  codeforge:     { profile: codeforge,     skills: [github-pr-workflow] }
  researcher:    { profile: researcher,    skills: [linkup-research, arxiv, blogwatcher] }
  qabot:         { profile: qabot,         skills: [dogfood, github-pr-workflow] }
  hsbcmm:        { profile: hsbc-credit-card-manager, skills: [hsbc-credit-card-manager] }
```

The dispatch contract lives in the `agent-orchestration` skill; personalities in `sub-agent-personalities`; hard rules in `sub-agent-guardrails`. Each agent gets a goal + context; returns a short bullet summary.

## Profiles (persistent contexts — each is a Bot)

Persistent contexts carrying their own memory, skills, and config across sessions. Every specialist is a real profile visible in the Hermes desktop **Bots** tab:

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
```

## Cron Jobs

Hermes cron runs scheduled jobs. Reference: https://hermes-agent.nousresearch.com/docs

```yaml
cron:
  default_delivery: discord     # Discord primary (Telegram banned in India → fan out here)
  jobs:
    - name: Daily AI Brief
      schedule: "0 7 * * *"     # 7am IST
      skills: [arxiv, blogwatcher]
    - name: Daily AI Newsletter Email
      schedule: "0 8 * * *"
      deliver: local            # → saved for email send
    - name: Daily WMT Stock Price
      schedule: "30 0 * * 1-5"  # 6am IST Mon–Fri
    - name: Ultrahuman sync + insights
      schedule: "30 6 * * *"
      script: sync_then_insights.py
      no_agent: true
    - name: Daily Stock Prediction
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

## MCP + Ops Integrations

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

Telegram is banned in India; cron deliveries to Telegram route to Discord `#general` for inline rendering.

```yaml
delivery:
  fallbacks:
    - platform: telegram
      route_to: discord
      channel: "#general"
```

## Security Reminders

- Never commit this file with real API keys
- Use environment variable substitution: `${DASHSCOPE_API_KEY}`
- macOS credentials (VNC etc.) are passed via env vars at runtime only, never persisted to disk
- Hermes respects `.env` files at the workspace root
- Each profile has its own secrets — don't share

---

*Template last updated August 2026*