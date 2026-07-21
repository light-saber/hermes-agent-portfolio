# Hermes Agent Configuration Template

This is a template configuration. Copy to `config.yaml` (rename to `.yaml`) and customize with your values.

## Usage

```bash
# Note: this template is .md for readability; rename to .yaml after copying
cp config/templates/config.example.md config/config.yaml
# Edit the file with your API keys and preferences
```

## Model Configuration

```yaml
model:
  default: MiniMax-M3            # Momo's default model
  provider: minimax
  api_key: YOUR_MINIMAX_API_KEY
  # Fallback chain — used when default is unavailable
  fallbacks:
    - anthropic/claude-sonnet-4
    - openai/gpt-4o
```

### Provider Notes
- **Anthropic** — primary reasoning; used for nuanced multi-step work
- **OpenAI Codex** — used for code-generation tasks via the codex skill
- **MiniMax-M3** — daily-driver for cron jobs, briefings, short Q&A (cost-effective at scale)

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

Two-tier memory. Hermes memory is the always-on budget (~2,200 chars); OpenViking is the long-term semantic store (unlimited).

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

Momo is the orchestrator. Define which specialists are available:

```yaml
subagents:
  stockman:
    skills: [stockman, stock-prediction-model]
  taxbuddy:
    profile: tax-assist          # persistent profile for sustained ITR work
    skills: [india-rsu-tax-filing]
  homebase:
    skills: []                    # reads case files under ~/.hermes/cases/homebase/
  healthguard:
    skills: [ultrahuman-insights]
  codeforge:
    skills: [github-pr-workflow]
  researcher:
    skills: [linkup-research, arxiv, blogwatcher]
```

The dispatch contract lives in the `sub-agent-dispatch` skill. Each agent gets a goal + context; returns a 3-5 bullet summary.

## Profiles

Persistent contexts that carry their own memory, skills, and config across sessions.

```yaml
profiles:
  default:
    description: Main Momo profile (current)
  tax-assist:
    description: Sustained ITR work
    workspace: ~/.hermes/profiles/tax-assist/workspace/
  hsbc-credit-card-manager:
    description: Credit card statement analysis
```

## Cron Jobs

Hermes cron runs scheduled jobs. Reference: https://hermes-agent.nousresearch.com/docs

```yaml
cron:
  default_delivery: discord     # Discord primary
  jobs:
    - name: Daily AI Brief
      schedule: "0 7 * * *"     # 7am IST
      skills: [arxiv, blogwatcher]
    - name: Daily Ultrahuman
      schedule: "0 7 * * *"
      skills: [ultrahuman-insights]
    - name: Daily Stock Prediction
      schedule: "30 3 * * 1-5"  # 9am IST Mon-Fri
      skills: [stock-prediction-model, stockman]
    - name: HomeBase Watchdog
      schedule: "0 10 * * *"    # 10am IST
      skills: [sub-agent-dispatch]
```

## MCP Integrations

```yaml
mcp:
  kite:                          # Zerodha Kite
    enabled: true
  github:
    enabled: true
  discord:
    enabled: true
  discord_admin:
    enabled: true
  openhue:                       # Philips Hue
    enabled: true
  apple_reminders:
    enabled: true
```

## Platform Integration

```yaml
telegram:
  bot_token: YOUR_TELEGRAM_BOT_TOKEN
  allowed_chats:
    - YOUR_CHAT_ID

discord:
  bot_token: YOUR_DISCORD_BOT_TOKEN
  server_id: YOUR_SERVER_ID
  channel_prompts: {}

photon:                           # iMessage via Photon
  enabled: true
```

## Delivery Routing

Telegram is banned in India; cron deliveries to Telegram routes to Discord `#general` for inline rendering.

```yaml
delivery:
  fallbacks:
    - platform: telegram
      route_to: discord
      channel: "#general"
```

## Additional Providers

```yaml
openrouter:
  api_key: YOUR_OPENROUTER_API_KEY
```

## Security Reminders

- Never commit this file with real API keys
- Use environment variable substitution: `${MINIMAX_API_KEY}`
- Hermes respects `.env` files at the workspace root
- Each profile has its own secrets — don't share

---

*Template last updated July 2026*