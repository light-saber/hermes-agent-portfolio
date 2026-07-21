# Hermes Agent Architecture

High-level system architecture for the Hermes Agent personal assistant system. Last updated: July 2026.

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Hermes Agent Core                       │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  Skills  │  │  Memory  │  │  Cron    │  │   MCP    │    │
│  │ System   │  │  Layer   │  │Scheduler │  │  Tools   │    │
│  │  89 / 33 │  │ 2-tier   │  │  14 jobs │  │          │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       │             │             │             │           │
│  ┌────┴─────────────┴─────────────┴─────────────┴────┐     │
│  │          Tool Orchestration + Sub-agent          │     │
│  │                Dispatch Layer                     │     │
│  └─────────────────────┬───────────────────────────┘     │
├────────────────────────┼──────────────────────────────────┤
│            ┌───────────┴───────────┐                      │
│            │    LLM Providers      │                      │
│            │ Anthropic · OpenAI    │                      │
│            │ Codex · MiniMax-M3    │                      │
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

### 1. Hermes Agent Core — Momo (Chief of Staff)
- **Purpose**: Main agent orchestrator and primary chat-facing persona. Routes requests, manages conversation state, coordinates tool execution, and dispatches to sub-agents.
- **Responsibilities**: LLM interaction, tool call sequencing, error handling, multi-turn reasoning, sub-agent dispatch
- **Providers**: Anthropic Claude, OpenAI (via Codex), MiniMax-M3 — routed by task type

### 2. Sub-agent Roster (6 specialists)

Momo delegates non-trivial work to one of six specialist sub-agents via `delegate_task`. Each sub-agent operates in an isolated context window, returns a clean summary back to Momo, and Momo presents it to the user.

| # | Agent | Domain |
|---|-------|--------|
| 1 | **StockMan** | Ad-hoc equity research, thesis reviews, sector deep-dives |
| 2 | **TaxBuddy** | Form16/26AS/AIS reconciliation, capital gains, ITR-2 prep (profile: `tax-assist`) |
| 3 | **HomeBase** | Property escalations (builder handovers, maintenance), home loan amortization, watchdog duties |
| 4 | **HealthGuard** | Health insurance policy, claims, wearable trends, family vaccinations |
| 5 | **CodeForge** | Side-project scoping → Claude Code handoff brief |
| 6 | **Researcher** | Deep-dive research (vaccines, tech, policy) |

The dispatch playbook lives in the `sub-agent-dispatch` skill. Default behavior: any multi-step or research-heavy ask → dispatch to the matching agent. Inline: simple Q&A, single tool calls, cron-managed workflows.

### 3. Skills System (89 skills, 33 categories)
- **Purpose**: Modular capability packages — each skill is a self-contained workflow
- **Structure**:
  - `SKILL.md` — definition, prerequisites, commands, pitfalls
  - `references/` — supporting docs
  - `templates/` — config snippets
  - `scripts/` — helper scripts
- **Loading**: On-demand per task (not all loaded at startup)
- **Categories**: autonomous-ai-agents, creative, financial-analysis, github, mlops, productivity, research, software-development, stock-prediction-model, ultrahuman-insights, sub-agent-dispatch, and 22 more

### 4. Memory Layer (Two-Tier)
- **Tier 1 — Hermes memory** (always-on, ~2,200 chars): small fixed-budget buffer injected into every system prompt. Holds durable preferences, rules, and pointers.
- **Tier 2 — OpenViking** (`viking://`): vector-indexed semantic knowledge base. Holds case files, entity profiles, event history, full statements. Retrieved only when explicitly searched.
- **User Profile**: Preferences, location, work details, tool conventions (never shared externally)

### 5. Cron Scheduler (14 active jobs)
- **Purpose**: Reliable time-based task execution — not just reminders, but full agentic workflows
- **Features**: Recurring and one-shot jobs, multi-platform delivery, script-based watchdog mode
- **Active Jobs**:

| Job | Schedule | Skills Used |
|-----|----------|-------------|
| Daily AI Ecosystem Brief | 7:00am IST daily | arxiv, blogwatcher |
| Daily Ultrahuman Insights | 7:00am IST daily | ultrahuman-insights |
| Daily Morning Prediction | 9:00am IST Mon–Fri | stock-prediction-model, stockman |
| Daily Prediction vs Actual | 3:45pm IST Mon–Fri | stockman |
| Daily WMT Stock Price | 6:00am IST Mon–Fri | — (terminal only) |
| Daily memes | 8:30am IST daily | gif-search |
| MailScout | 2:30pm IST daily | himalaya |
| Monthly Stock Screener | 1st of month, 9am IST | — (script) |
| Enhanced Screener — NSE Monthly | 1st of month, 3:30am UTC | — (script) |
| HSBC Premier Monthly Brief | 1st of month, midnight UTC | — (terminal + file) |
| HomeBase property watchdog | 10:00am IST daily | sub-agent-dispatch |
| Kimi subscription + cron migration | 18 Aug 2026 09:00 IST (one-shot) | — |
| Kimi signup backup reminder | 15 Aug 2026 09:00 IST (one-shot) | — |
| WhatsApp response monitor | every 60m (paused/disabled) | — (script) |

- **Delivery**: Discord primary; some jobs deliver to origin (current chat); HomeBase watchdog explicitly to Discord Home

### 6. MCP Tools (Model Context Protocol)
- **Purpose**: Structured integration with external services
- **Active Integrations**:
  - `Kite` — Zerodha trading: LTP, quotes, positions, orders, holdings, GTT orders
  - `GitHub` — REST API via gh CLI: repos, PRs, issues, code review
  - `Discord` — message send/reply/react
  - `Discord Admin` — channel/role management, member search, message pinning, thread creation
  - `OpenHue` — Philips Hue lights and scenes
  - `Apple Reminders` — via remindctl CLI

## Profiles (persistent contexts)

Hermes supports per-profile memory, skills, and config — useful for separating domains:

- `default` — main Momo profile (current, primary)
- `tax-assist` — sustained ITR work; carries tax workspace and documents across sessions. Used by TaxBuddy for ongoing reconciliation.
- `hsbc-credit-card-manager` — credit card statement analysis and rewards optimization. Cron delivers monthly brief to Discord `#credit-card-manager`.

## Platform Integrations

### Discord
- Primary home channel for cron job delivery
- Ideas channel (`#ideas`) — AI ecosystem briefs
- StockMan output — predictions and analysis
- HomeBase watchdog — open-escalation alerts
- Voice effects and ambient sounds (per-server)
- Telegram deliveries fan out here (Telegram banned in India, deliveries routed to Discord)

### Photon (iMessage)
- Mobile-first channel via Photon Spectrum
- Home delivery for on-the-go access
- Supports text, markdown, and voice memos

### Web Browser
- Full CDP-based browser automation
- Used for: dogfood QA, web scraping, interactive page automation

## Data Flow (with sub-agent dispatch)

```
User Message (Discord / Telegram / Photon)
    │
    ▼
Platform Adapter
    │
    ▼
Momo (Chief of Staff)
    │
    ├─▶ Skill Selection (match task to skill)
    ├─▶ Memory Injection (Hermes tier-1 + relevant OpenViking retrieval)
    ├─▶ Sub-agent Decision
    │       │
    │       └─▶ if multi-step → delegate_task(StockMan | TaxBuddy |
    │                          HomeBase | HealthGuard | CodeForge |
    │                          Researcher)
    │              │
    │              └─▶ Sub-agent works in isolated context
    │                     │
    │                     ▼
    │                 Returns summary to Momo
    │
    ├─▶ LLM Processing (MiniMax-M3 default)
    └─▶ Tool Execution (MCP tools, terminal, file, web)
    │
    ▼
Response (markdown / structured data, 3-5 bullet summary)
    │
    ▼
Platform Adapter
    │
    ▼
User (same platform or fan-out to all home channels)
```

## Skill System Deep Dive

### Sub-agent Dispatch Pattern

Momo follows a simple rule: **multi-step or research-heavy asks go to sub-agents; trivial asks stay inline.** The dispatch template (lives in `sub-agent-dispatch` skill) captures the goal + context per agent, lists the skills each agent should load, and standardizes the output shape. Sub-agents never re-dispatch — they're leaves.

### Financial Analysis (StockMan)
Dedicated analyst persona running on MiniMax-M3:
- Nifty trend first, then sector checks
- Banks sector on credit growth; Power most reliable sector signal
- Daily prediction → daily comparison → monthly accuracy tracking
- 24 holdings across gold, banking, NBFC, steel, power, IT, consumption
- **Two paths**:
  1. Scheduled (cron): daily prediction + vs actual + monthly screener
  2. On-demand: Momo dispatches `StockMan` via `delegate_task` when Sachin asks "should I buy X"

### HomeBase (Watchdog Pattern)
HomeBase is the only sub-agent with a **dedicated cron** — it watches open property escalations and alerts when deadlines approach. Case files under `~/.hermes/cases/homebase/` carry status, timeline, and pending actions.

### AI Ecosystem Monitoring
Daily brief at 7am IST using three research skills:
- `arxiv` — recent ML/AI papers
- `github-trending-scout` — trending repos, new stars/forks
- `blogwatcher` — RSS feeds on AI/tech blogs

## Security Architecture

```
┌─────────────────────────────────────┐
│       Environment Variables         │
│  (API keys, tokens, secrets)        │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│     Config Loading Layer            │
│   (reads .yaml, applies env vars)   │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│    Hermes Agent Runtime             │
│   (skills, cron, tools, memory,     │
│    sub-agent dispatch)              │
└─────────────────────────────────────┘
```

### Best Practices Enforced
- Never commit secrets — `.gitignore` covers all config files
- Environment variable substitution in configs
- No secrets stored in memory files or skills
- API keys scoped per integration (Kite, GitHub, Hue, etc.)
- Case files for sensitive contexts (property escalations, ITR prep) live in `~/.hermes/cases/` — not committed

## Technology Stack

| Component | Technology |
|-----------|------------|
| Agent Core | Hermes Agent (Nous Research) |
| Chief-of-staff persona | Momo |
| Sub-agent mechanism | `delegate_task` (leaf role, isolated context) |
| LLM Providers | Anthropic Claude, OpenAI Codex, MiniMax-M3 |
| Memory | OpenViking (semantic KB) + Hermes always-on memory |
| Scheduling | Hermes Cron (built-in) |
| Profiles | default, tax-assist, hsbc-credit-card-manager |
| Platforms | Discord, Photon (iMessage), Telegram (routed to Discord) |
| Trading | Zerodha Kite MCP |
| Hosting | Linux VPS (Hostinger) |
| Skill Count | 89 across 33 categories |

## Scalability Profile

### Current Setup (Single User, Production)
- Runs autonomously on VPS — no laptop required
- 14 cron jobs running on schedule
- All platforms connected simultaneously
- ~89 skills available on demand
- 6 sub-agents available on demand
- OpenViking KB holds long-term memory

### What This Demonstrates
- Chief-of-staff + sub-agent orchestration at personal scale
- Reliable long-running automation (not just one-off tasks)
- Cross-platform message routing
- Composable skill architecture
- Security-conscious configuration

---

*Architecture as of July 2026*