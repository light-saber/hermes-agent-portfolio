# Hermes Agent Architecture

High-level system architecture for the Hermes Agent personal assistant system. Last updated: June 2026.

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Hermes Agent Core                       │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  Skills  │  │  Memory  │  │  Cron    │  │   MCP    │    │
│  │ System   │  │  Layer   │  │Scheduler │  │  Tools   │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       │             │             │             │           │
│  ┌────┴─────────────┴─────────────┴─────────────┴────┐     │
│  │              Tool Orchestration                   │     │
│  └─────────────────────┬───────────────────────────┘     │
├────────────────────────┼──────────────────────────────────┤
│            ┌───────────┴───────────┐                      │
│            │    LLM Providers      │                      │
│            │ Anthropic · OpenAI    │                      │
│            │    Codex · MiniMax    │                      │
│            └──────────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
   ┌─────────┐         ┌─────────┐         ┌─────────┐
   │ Discord │         │ Photon  │         │  Web    │
   │  Bot    │         │(iMessage)         │ Browser │
   └─────────┘         └─────────┘         └─────────┘
```

## Core Components

### 1. Hermes Agent Core
- **Purpose**: Main agent orchestrator — routes requests, manages conversation state, coordinates tool execution
- **Responsibilities**: LLM interaction, tool call sequencing, error handling, multi-turn reasoning
- **Providers**: Anthropic Claude, OpenAI (via Codex), MiniMax — routed by task type

### 2. Skills System (84 skills, 20 categories)
- **Purpose**: Modular capability packages — each skill is a self-contained workflow
- **Structure**: 
  - `SKILL.md` — definition, prerequisites, commands, pitfalls
  - `references/` — supporting docs
  - `templates/` — config snippets
  - `scripts/` — helper scripts
- **Loading**: On-demand per task (not all loaded at startup)
- **Categories**: autonomous-ai-agents, creative, financial-analysis, github, mlops, productivity, research, software-development, and 12 more

### 3. Memory Layer (Two-Tier)
- **Short-term**: Session context injected every turn (~1,700 chars of user/memory profile)
- **Long-term**: OpenViking semantic knowledge base (`viking://`) — persistent across sessions
- **User Profile**: Preferences, location, work details, tool conventions (never shared externally)

### 4. Cron Scheduler (7 active jobs)
- **Purpose**: Reliable time-based task execution — not just reminders, but full agentic workflows
- **Features**: Recurring and one-shot jobs, multi-platform delivery, script-based watchdog mode
- **Active Jobs**:

| Job | Schedule | Skills Used |
|-----|----------|-------------|
| Daily AI Ecosystem Brief | 7:00am IST daily | arxiv, github, blogwatcher |
| Daily Morning Prediction | 9:00am IST Mon–Fri | stockman |
| Daily Prediction vs Actual | 3:00pm IST Mon–Fri | stockman |
| Daily WMT Stock Price | 6:00am IST Mon–Fri | stock-price |
| Portfolio Prediction vs Actual | 3:00pm IST Mon–Fri | stockman |
| Monthly Stock Screener | 1st of month, 9am IST | — (script) |
| MailScout (expense tracking) | 2:30pm IST daily | himalaya |

- **Delivery**: Discord primary; some jobs also deliver to origin (current chat)

### 5. MCP Tools (Model Context Protocol)
- **Purpose**: Structured integration with external services
- **Active Integrations**:
  - `Kite` — Zerodha trading: LTP, quotes, positions, orders, holdings, GTT orders
  - `GitHub` — REST API via gh CLI: repos, PRs, issues, code review
  - `OpenHue` — Philips Hue lights and scenes
  - `Apple Reminders` — via remindctl CLI

## Platform Integrations

### Discord
- Primary home channel for cron job delivery
- Ideas channel (`#ideas`) — AI ecosystem briefs
- StockMan output — predictions and analysis
- Voice effects and ambient sounds (per-server)

### Photon (iMessage)
- Mobile-first channel via Photon Spectrum
- Home delivery for on-the-go access
- Supports text, markdown, and voice memos

### Web Browser
- Full CDP-based browser automation
- Used for: dogfood QA, web scraping, interactive page automation

## Data Flow

```
User Message (Discord / Telegram / Photon)
    │
    ▼
Platform Adapter
    │
    ▼
Hermes Agent Core
    │
    ├─▶ Skill Selection (match task to skill)
    ├─▶ Memory Injection (user profile + session context)
    ├─▶ LLM Processing (reasoning + tool planning)
    └─▶ Tool Execution (MCP tools, terminal, file, web)
    │
    ▼
Response (markdown / structured data)
    │
    ▼
Platform Adapter
    │
    ▼
User (same platform or fan-out to all home channels)
```

## Skill System Deep Dive

### Autonomous AI Agents
Explicit two-stage workflow:
1. **Planning stage** (main assistant) — ideation, scoping, architecture, tradeoffs
2. **Execution stage** (Claude Code / Codex / OpenCode) — only after explicit user approval

This separation prevents the main assistant from jumping straight to code and keeps human judgment in the loop.

### Financial Analysis (StockMan)
Dedicated analyst persona running on MiniMax-M2.1:
- Nifty trend first, then sector checks
- Banks sector on credit growth; Power most reliable sector signal
- Daily prediction → daily comparison → monthly accuracy tracking
- 24 holdings across gold, banking, NBFC, steel, power, IT, consumption

### AI Ecosystem Monitoring
Daily brief at 7am IST using three research skills:
- `arxiv` — recent ML/AI papers
- `github` — trending repos, new stars/forks
- `blogwatcher` — RSS feeds on AI/tech blogs

## Security Architecture

```
┌─────────────────────────────────────┐
│       Environment Variables         │
│  (API keys, tokens, secrets)        │
└────────────────┬──────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│     Config Loading Layer            │
│   (reads .yaml, applies env vars)  │
└────────────────┬──────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│    Hermes Agent Runtime             │
│   (skills, cron, tools, memory)    │
└─────────────────────────────────────┘
```

### Best Practices Enforced
- Never commit secrets — `.gitignore` covers all config files
- Environment variable substitution in configs
- No secrets stored in memory files or skills
- API keys scoped per integration (Kite, GitHub, Hue, etc.)

## Technology Stack

| Component | Technology |
|-----------|------------|
| Agent Core | Hermes Agent (Nous Research) |
| LLM Providers | Anthropic Claude, OpenAI Codex, MiniMax-M2.1 |
| Memory | OpenViking (semantic KB) + session context |
| Scheduling | Hermes Cron (built-in) |
| Platforms | Discord, Photon (iMessage), Web Browser |
| Trading | Zerodha Kite MCP |
| Hosting | Linux VPS (Hostinger) |
| Skill Count | 84 across 20 categories |

## Scalability Profile

### Current Setup (Single User, Production)
- Runs autonomously on VPS — no laptop required
- 7 cron jobs running on schedule
- All platforms connected simultaneously
- ~84 skills available on demand
- OpenViking KB holds long-term memory

### What This Demonstrates
- Multi-agent orchestration at personal scale
- Reliable long-running automation (not just one-off tasks)
- Cross-platform message routing
- Composable skill architecture
- Security-conscious configuration

---

*Architecture as of June 2026*
