# Hermes Agent Architecture

High-level system architecture for the Hermes Agent personal assistant system. Last updated: August 2026.

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Hermes Agent Core                       │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  Skills  │  │  Memory  │  │  Cron    │  │   MCP    │    │
│  │ System   │  │  Layer   │  │Scheduler │  │  Tools   │    │
│  │ 145 / 52 │  │ 2-tier   │  │ ~30 jobs │  │          │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       │             │             │             │           │
│  ┌────┴─────────────┴─────────────┴─────────────┴────┐     │
│  │          Tool Orchestration + Sub-agent          │     │
│  │          Dispatch Layer (10 specialists)         │     │
│  └─────────────────────┬───────────────────────────┘     │
├────────────────────────┼──────────────────────────────────┤
│            ┌───────────┴───────────┐                      │
│            │    LLM Providers      │                      │
│            │ Alibaba/DashScope     │                      │
│            │ (DeepSeek V4 Flash)   │                      │
│            │ + Nous aux/image      │                      │
│            └──────────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
   ┌─────────┐         ┌─────────┐         ┌─────────┐
   │ Discord │         │ WhatsApp│         │ Photon  │
   │ Telegram│         │ wa-brg  │         │(iMessage│
   │ (fanout)│         │    :8765│         │         │
   └─────────┘         └────┬────┘         └─────────┘
                            │
        + OwnTracks MQTT (location) · Mac Mini (SSH/CDP) · Web Browser
```

## Core Components

### 1. Hermes Agent Core — Momo (Chief of Staff)
- **Purpose**: Main agent orchestrator and primary chat-facing persona. Routes requests, manages conversation state, coordinates tool execution, and dispatches to sub-agents.
- **Responsibilities**: LLM interaction, tool call sequencing, error handling, multi-turn reasoning, sub-agent dispatch
- **Provider**: Alibaba (DeepSeek V4 Flash via DashScope) for the main agent and all crons; Nous for image generation and auxiliary vision/web-extract/compression.

### 2. Sub-agent Roster (10 specialists)

Momo delegates non-trivial work to one of ten specialist sub-agents via `delegate_task`. Each operates in an isolated context window, returns a clean summary, and also runs as a real Hermes profile (a desktop Bot). Roster: MacPilot, StockMan, TaxBuddy, HomeBase, HealthGuard, FamilyDoc, CodeForge, Researcher, QABot, HSBC Card Manager.

| # | Agent | Domain |
|---|-------|--------|
| 1 | **MacPilot** | Drives Sachin's Mac (Safari, files, screenshots, shell) over Tailscale — SSH + AppleScript + CDP |
| 2 | **StockMan** | Equity research, thesis reviews, sector deep-dives, daily portfolio prediction |
| 3 | **TaxBuddy** | Form16/26AS reconciliation, capital gains, ITR-2 prep, advance tax (profile: `tax-assist`) |
| 4 | **HomeBase** | Property escalations, home loan amortization, watchdog duties |
| 5 | **HealthGuard** | Health insurance, claims, wearable trends, vaccinations |
| 6 | **FamilyDoc** | Family physician triage — symptoms, Rx, vaccine info, labelled "AI diagnosis" |
| 7 | **CodeForge** | Side-project scoping → Claude Code handoff brief (never writes code) |
| 8 | **Researcher** | Multi-source deep dives with citations |
| 9 | **QABot** | QA after builds — dogfood browser testing, evidence-led verdicts |
| 10 | **HSBC Card Manager** | HSBC Premier credit card statement analysis & rewards |

The dispatch playbook lives in the `agent-orchestration` skill; `sub-agent-personalities` defines each agent's voice; `sub-agent-guardrails` holds hard rules. Default behavior: any multi-step or research-heavy ask → dispatch to the matching agent. Inline: simple Q&A, single tool calls, cron-managed workflows.

### 3. Skills System (~145 skills, 52 categories)
- **Purpose**: Modular capability packages — each skill is a self-contained workflow
- **Structure**: `SKILL.md` (definition/prereqs/commands/pitfalls) + optional `references/`, `templates/`, `scripts/`
- **Loading**: On-demand per task (not all loaded at startup)
- **Archive**: `.archive/` holds last-generation skills that were absorbed into umbrellas or pruned — excluded from the active count
- **Categories**: productivity (27), software-development (17), research (11), autonomous-ai-agents (10), financial-analysis (8), media (7), mlops (6), and 45 more

### 4. Memory Layer (Two-Tier)
- **Tier 1 — Hermes memory** (always-on, ~2,200 chars): fixed-budget buffer injected into every system prompt. Holds durable preferences, rules, pointers.
- **Tier 2 — OpenViking** (`viking://`): vector-indexed semantic knowledge base (at 127.0.0.1:1933) holding case files, entity profiles, event history, full statements. Retrieved only when searched. Monitored by a watchdog cron.
- **User Profile**: Preferences, location, work details, tool conventions (never shared externally)

### 5. Cron Scheduler (~30 active jobs, 38 registered)
- **Purpose**: Reliable time-based task execution — not just reminders, but full agentic workflows, plus script-only watchdog mode (`no_agent`).
- **Features**: Recurring and one-shot jobs, multi-platform delivery, script-based watchdogs, model pinning per job.
- **Note**: cron sessions cannot call `delegate_task` — each cron prompt is a thin self-contained orchestrator.
- **Highlights**: daily AI brief + newsletter, MailScout expense digest (dedupes card-bill repayments vs consumption), stock predictions + vs-actual, portfolio activity watchdogs (NSE intraday/close, WMT close), IBKR tracker, minitrader paper pick, HomeBase watchdog, pregnancy milestone one-shots, advance-tax reminders, WhatsApp group nudges, OwnTracks-gated office asks, monthly screeners + HSBC brief + subscription audit, memory-system watchdog, upstream PR tracker.

### 6. MCP Tools (Model Context Protocol)
- **Purpose**: Structured integration with external services
- **Active Integrations**:
  - `Kite` — Zerodha trading: LTP, quotes, positions, orders, holdings, GTT orders (auth is in-memory — prediction crons prefer yfinance fallback for fragility)
  - `GitHub` — REST API via gh CLI: repos, PRs, issues, code review
  - `Discord` — message send/reply/react · `Discord Admin` — channel/role mgmt, pinning, threads
  - `IBKR` — Interactive Brokers via Claude Code CLI + IBKR MCP
  - `OpenHue` — Philips Hue lights and scenes
  - Plus non-MCP ops infrastructure: WhatsApp wa-bridge (:8765), OwnTracks MQTT broker, Mac SSH/CDP

## Profiles (persistent contexts — each a Bot)

Every specialist is a real `~/.hermes/profiles/<name>/` profile with its own SOUL.md persona + profile.yaml, visible in the Hermes desktop **Bots** tab:

- `default` — main Momo profile (orchestrator, primary)
- `stockman`, `homebase`, `healthguard`, `familydoc`, `codeforge`, `researcher`, `qabot`, `macpilot` — specialist Bots
- `tax-assist` — sustained ITR work; TaxBuddy's profile
- `hsbc-credit-card-manager` — card statement analysis + rewards

## Platform Integrations

### Discord
- Primary home channel for cron delivery
- Sub-bot outputs routed per channel (pregnancy milestones, HSBC brief, watchdogs, minitrader)
- Telegram deliveries fan out here (Telegram banned in India)

### WhatsApp (wa-bridge)
- VPS `wa-bridge` on :8765 for read + send
- Group nudges ("tiffin pe charcha": Friday cab-booking, lunch asks)
- Office-presence asks gated on OwnTracks arrival detection

### Photon (iMessage)
- Mobile-first channel via Photon Spectrum

### OwnTracks (Location)
- Self-hosted MQTT broker (mosquitto, Let's Encrypt TLS, password auth) on the VPS
- Replaced Google/Apple location APIs (none usable); reverse-geocodes phone fixes, drives office-presence automations

### Mac (MacPilot)
- Full desktop control over Tailscale (SSH key-based, AppleScript, CDP browser control)
- Shopping/Amazon tasks routed through MacPilot rather than a VPS browser

### Web Browser
- Full CDP-based automation; used for dogfood QA, scraping, interactive automation

## Data Flow (with sub-agent dispatch)

```
User Message (Discord / WhatsApp / Photon / Telegram→Discord)
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
    │       └─▶ if multi-step → delegate_task(MacPilot | StockMan |
    │                          TaxBuddy | HomeBase | HealthGuard |
    │                          FamilyDoc | CodeForge | Researcher |
    │                          QABot | HSBC Card Manager)
    │              │
    │              └─▶ Sub-agent works in isolated context
    │                     │
    │                     ▼
    │                 Returns summary to Momo
    │
    ├─▶ LLM Processing (Alibaba / DeepSeek V4 Flash)
    └─▶ Tool Execution (MCP tools, terminal, file, web)
    │
    ▼
Response (markdown / structured data, short bullet summary)
    │
    ▼
Platform Adapter
    │
    ▼
User (same platform or fan-out to all home channels)
```

## Skill System Deep Dive

### Sub-agent Dispatch Pattern
Momo's rule: **multi-step or research-heavy asks go to sub-agents; trivial asks stay inline.** The `agent-orchestration` skill captures goal + context templates per agent, the skills each should load, and standardizes the output shape. Sub-agents never re-dispatch — they're leaves. Every profile/Bot carries its persona from `sub-agent-personalities` and hard rules from `sub-agent-guardrails`.

### Financial Analysis (StockMan + Minitrader)
- Nifty trend first, then sector checks; Banks on credit growth; Power most reliable
- Daily prediction → daily comparison → monthly accuracy tracking
- Prediction crons use a yfinance fallback (`portfolio_market_fallback.py`) as primary to drop Kite's in-memory-auth fragility
- **Minitrader**: dual live + paper long-term books on Kite, CNC-only, human-in-the-loop buy gate
- **Portfolio activity watchdog**: low-noise price/volume anomaly monitor (STALE_HOLDINGS_HOURS=720; success = analysed, not signal)

### HomeBase (Watchdog Pattern)
HomeBase is the only watchdog sub-agent with a dedicated cron. Alerts keyed to (case, trigger, deadline, state) so they're idempotent — never use case-level status as a proxy for a deliverable-owned deadline. Case files under `~/.hermes/cases/homebase/`.

### AI Ecosystem Monitoring
Daily brief at 7am IST: `arxiv` (recent ML/AI papers), `blogwatcher` (RSS/AI blogs), plus a newsletter email at 8am. GitHub trending via `github-research`.

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
- Never commit secrets — `.gitignore` covers all config files; env-var substitution in configs
- No secrets in memory files or skills
- API keys scoped per integration; VNC/macOS creds never persisted to disk (passed via env var)
- Case files (property escalations, ITR prep, pregnancy milestones) and holdings live under `~/.hermes/cases/` and `~/.hermes/profiles/` — never committed
- Prompt-injection guard for MacPilot: no following instructions from web pages/screenshots

## Technology Stack

| Component | Technology |
|-----------|------------|
| Agent Core | Hermes Agent (Nous Research) |
| Chief-of-staff persona | Momo |
| Sub-agent mechanism | `delegate_task` (leaf role, isolated context) + per-agent profiles/Bots |
| LLM Provider | Alibaba DeepSeek V4 Flash (DashScope) ; Nous (image gen, aux vision/extract) |
| Memory | OpenViking (semantic KB, 127.0.0.1:1933) + Hermes always-on memory |
| Scheduling | Hermes Cron (built-in), script-only watchdog mode |
| Profiles | default + 10 specialist Bots |
| Platforms | Discord, WhatsApp (wa-bridge), Telegram (→Discord), Photon (iMessage) |
| Location | OwnTracks + mosquitto MQTT (TLS, password auth) |
| Trading | Zerodha Kite MCP (+ yfinance fallback), IBKR MCP, Minitrader |
| Remote ops | Mac Mini over Tailscale (SSH, AppleScript, CDP) |
| Hosting | Linux VPS (Hostinger) |
| Skill Count | ~145 across 52 categories (active) |

## Scalability Profile

### Current Setup (Single User, Production)
- Runs autonomously on VPS + Mac — no single point of dependency
- ~30 cron jobs; 10 specialist sub-agents/Bots available on demand
- All platforms connected simultaneously
- OpenViking KB holds long-term memory; watchdog monitors its health

### What This Demonstrates
- Chief-of-staff + sub-agent orchestration at personal scale
- Reliable long-running automation, including script-only watchdogs
- Cross-platform message routing with India-specific constraints (Telegram ban)
- Self-hosted production infra (MQTT location, wa-bridge, Tailscale Mac access)
- Composable skill architecture (145 active skills)
- Security-conscious configuration

---

*Architecture as of August 2026*