# Hermes Agent Architecture

High-level system architecture for the Hermes Agent personal assistant system. Last reviewed: November 2026 (Hermes Agent v0.23.2).

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Hermes Agent Core                       │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  Skills  │  │  Memory  │  │  Cron    │  │   MCP    │    │
│  │ System   │  │  Layer   │  │Scheduler │  │  Tools   │    │
│  │ 129 / 53 │  │ 2-tier   │  │35 enabled│  │          │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       │             │             │             │           │
│  ┌────┴─────────────┴─────────────┴─────────────┴────┐     │
│  │          Tool Orchestration + Specialist          │     │
│  │ Dispatch + Kanban queue (10 agents + profile worker) │    │
│  └─────────────────────┬───────────────────────────┘     │
├────────────────────────┼──────────────────────────────────┤
│            ┌───────────┴───────────┐                      │
│            │    LLM Providers      │                      │
│            │ Nous                  │                      │
│            │ openai/gpt-6-luna      │                      │
│            │ + profile overrides    │                      │
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

### 1. Hermes Agent Core - Momo (Chief of Staff)
- **Purpose**: Main agent orchestrator and primary chat-facing persona. Routes requests, manages conversation state, coordinates tool execution, and dispatches to sub-agents.
- **Responsibilities**: LLM interaction, tool call sequencing, error handling, multi-turn reasoning, sub-agent dispatch
- **Provider**: Nous. Main agent and delegation default to `openai/gpt-6-luna`; profile and cron overrides are explicit. Auxiliary tasks are individually configured; the previous shared LongCat route was reported as delisted, and curator's latest LLM review reports it unavailable.

### 2. Specialist Roster (10 `delegate_task` agents + 1 profile worker)

Momo delegates non-trivial work to ten specialist agents via `delegate_task`. Each operates in an isolated context window and returns a clean summary. Wildlife-photo caption drafting follows a distinct route: a local helper sends image observations and only actually extracted EXIF to the dedicated `wildlifephoto` profile, which returns drafts and never publishes. Specialist profiles are also available as Hermes desktop Bots.

See [specialist routing](specialists.md) for the dispatch boundary, role list, and guardrails.

Hermes Kanban work queues persist profile-assigned tasks, support dependencies and review, and run through the gateway dispatcher; they are separate from bounded `delegate_task` calls. The queue model and workflow are documented as system architecture, but the default board/task count has not been rechecked in this review.

| # | Specialist | Domain / route |
|---|-------|--------|
| 1 | **MacPilot** | Drives the user's Mac (Safari, files, screenshots, shell) over Tailscale - SSH + AppleScript + CDP |
| 2 | **StockMan** | Equity research, thesis reviews, sector deep-dives, daily portfolio prediction |
| 3 | **TaxBuddy** | Form16/26AS reconciliation, capital gains, ITR-2 prep, advance tax (profile: `tax-assist`) |
| 4 | **HomeBase** | Property escalations, home loan amortization, watchdog duties |
| 5 | **HealthGuard** | Health insurance, claims, wearable trends, vaccinations |
| 6 | **FamilyDoc** | Family physician triage - symptoms, Rx, vaccine info, labelled "AI diagnosis" |
| 7 | **CodeForge** | Side-project scoping → Claude Code handoff brief (never writes code) |
| 8 | **Researcher** | Multi-source deep dives with citations |
| 9 | **QABot** | QA after builds - dogfood browser testing, evidence-led verdicts |
| 10 | **HSBC Card Manager** | HSBC Premier credit card statement analysis & rewards |
| 11 | **Feather / WildlifePhoto** | Image-grounded wildlife caption drafting; separate profile worker, draft-only |

The `agent-orchestration` skill defines dispatch. `sub-agent-personalities` defines agent voice; `sub-agent-guardrails` holds hard rules. Wildlife captions use a separate helper and profile, not `delegate_task`. Default behavior: multi-step or research-heavy asks go to the matching specialist; simple Q&A, single tool calls, and cron-managed workflows stay inline.

### 3. Skills System (129 enabled shared skills, 53 registry categories)
- **Purpose**: Modular capability packages - each skill is a self-contained workflow
- **Structure**: `SKILL.md` (definition/prereqs/commands/pitfalls) + optional `references/`, `templates/`, `scripts/`
- **Loading**: On-demand per task (not all loaded at startup)
- **Inventory**: `SKILLS.md` counts skills shown by `hermes skills list --source all --enabled-only`; disabled and profile-local skills are excluded.
- **Largest categories**: productivity (17), software-development (12), research (11), financial-analysis (9), autonomous-ai-agents (8), smart-home (6)

### 4. Memory Layer (Two-Tier)
- **Tier 1 - Hermes memory** (always-on, ~2,200 chars): fixed-budget buffer injected into every system prompt. Holds durable preferences, rules, pointers.
- **Tier 2 - OpenViking** (`viking://`): vector-indexed semantic knowledge base (at 127.0.0.1:1933) holding case files, entity profiles, event history, full statements. Retrieved only when searched. Monitored by a watchdog cron.
- **User Profile**: Preferences, location, work details, tool conventions (never shared externally)

### 5. Cron Scheduler (35 enabled jobs, 39 registered)
- **Purpose**: Reliable time-based task execution - not just reminders, but full agentic workflows, plus script-only jobs (`no_agent`).
- **Features**: Recurring and one-shot jobs, multi-platform delivery, script-based watchdogs, model pinning per job.
- **Note**: cron sessions cannot call `delegate_task` - each cron prompt is a thin self-contained orchestrator.
- **Highlights**: unified morning digest, MailScout expense digest, stock predictions + vs-actual, portfolio activity watchdogs, Vested US portfolio snapshot, family-care milestone reminders, advance-tax checks + payment reminders, daily WhatsApp quiz, OwnTracks-gated commute tracker, MG EV charge reminders, watch drop/restock alerts, monthly screeners + HSBC brief + subscription audit, memory-system watchdog, upstream PR tracking, and long-term financial reminders. Office-arrival breakfast/lunch nudges and HN digest are paused.

### 6. Curator (skill lifecycle)
- **Status**: enabled, weekly schedule; current live status reports 27 active and 24 stale skills among 51 curator-managed skills, with no archived skills.
- **Scope**: lifecycle management for eligible agent-created skills; pinned skills are protected. It does not manage the broader enabled shared skill inventory.
- **Current operational note**: the last curator run's LLM review reported that `meituan/longcat-2.5-preview:free` is no longer available on Nous. The auxiliary config still references that model; automated LLM review may therefore be degraded until the route is replaced and verified.

### 7. MCP Tools (Model Context Protocol)
- **Purpose**: Structured integration with external services
- **Active Integrations**:
  - `Kite` - Zerodha trading: LTP, quotes, positions, orders, holdings, GTT orders (auth is in-memory - prediction crons prefer yfinance fallback for fragility)
  - `GitHub` - REST API via gh CLI: repos, PRs, issues, code review
  - `Discord` - message send/reply/react · `Discord Admin` - channel/role mgmt, pinning, threads
  - `OpenHue` - Philips Hue lights and scenes
  - Plus non-MCP ops infrastructure: WhatsApp wa-bridge (:8765), OwnTracks MQTT broker, Mac SSH/CDP

## Profiles (specialist contexts)

Specialist profiles carry their own persona/configuration and are visible in the Hermes desktop **Bots** tab:

- `default` - main Momo profile (orchestrator, primary)
- `stockman`, `homebase`, `healthguard`, `familydoc`, `codeforge`, `researcher`, `qabot`, `macpilot` - specialist Bots
- `tax-assist` - sustained ITR work; TaxBuddy's profile
- `hsbc-credit-card-manager` - card statement analysis + rewards
- `wildlifephoto` - Feather wildlife-caption profile worker (separate from the ten `delegate_task` specialists)

There are 12 profiles total: the default profile plus 11 specialists. The dedicated wildlife-caption profile currently uses `openai/gpt-5.4-mini`; the other listed profiles use the fleet's `openai/gpt-6-luna` model.

## Platform Integrations

### Discord
- Primary home channel for cron delivery
- Sub-bot outputs routed per channel (pregnancy milestones, HSBC brief, watchdogs, minitrader)
- Telegram scheduled deliveries are routed to Discord in this setup.

### WhatsApp (wa-bridge)
- **WhatsApp** - self-hosted bridge for read + send
- Configured group nudges (Friday cab-booking and lunch asks)
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
    ├─▶ Specialist Decision
    ├─▶ if bounded multi-step → delegate_task(10 specialist agents)
    │       └─▶ isolated worker → summary to Momo
    ├─▶ if durable/profile-assigned → Kanban queue → dispatcher → worker profile
    │
    ├─▶ photo caption → local helper → wildlifephoto profile (image observations + verified EXIF)
    ├─▶ LLM Processing (Nous / openai/gpt-6-luna default; explicit overrides)
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

### Durable Kanban vs. `delegate_task`
Use `delegate_task` for bounded synchronous subtasks whose summary returns to Momo in the current turn. Use the Kanban board for durable tasks that should survive a gateway restart, have a named profile assignee, track dependencies or review, or need explicit task history. The dispatcher runs within the gateway; workers receive a board-scoped task context and isolated workspace. The default board task count was not verified in this review.

### Specialist Dispatch Pattern
Momo's rule: **multi-step or research-heavy asks go to specialists; trivial asks stay inline.** The `agent-orchestration` skill captures goal + context templates for `delegate_task` agents, the skills they should load, and output contracts. Those sub-agents are leaves. Wildlife captions use a separate profile-based worker. Specialist personas and hard rules live in `sub-agent-personalities` and `sub-agent-guardrails`.

### Financial Analysis (StockMan + Minitrader)
- Nifty trend first, then sector checks; Banks on credit growth; Power most reliable
- Daily prediction → daily comparison → monthly accuracy tracking
- Prediction crons use a yfinance fallback (`portfolio_market_fallback.py`) as primary to drop Kite's in-memory-auth fragility
- **Minitrader**: dual live + paper long-term books on Kite, CNC-only, human-in-the-loop buy gate
- **Portfolio activity watchdog**: low-noise price/volume anomaly monitor (STALE_HOLDINGS_HOURS=720; success = analysed, not signal)

### HomeBase (Watchdog Pattern)
HomeBase owns the property watchdog. Alerts are keyed to (case, trigger, deadline, state) so they are idempotent; never use case-level status as a proxy for a deliverable-owned deadline. Case files remain private.

### AI Ecosystem Monitoring
Unified morning digest (8:15am IST): `arxiv` (recent ML/AI papers), `blogwatcher` (RSS/AI blogs), and GitHub trending via `github-research`, delivered across Discord, email, and WhatsApp.

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
- Never commit secrets - `.gitignore` covers all config files; env-var substitution in configs
- No secrets in memory files or skills
- API keys scoped per integration; VNC/macOS creds never persisted to disk (passed via env var)
- Case files (property escalations, tax prep, family milestones) and holdings are private and never committed
- Prompt-injection guard for MacPilot: no following instructions from web pages/screenshots

## Technology Stack

| Component | Technology |
|-----------|------------|
| Agent Core | Hermes Agent (Nous Research) |
| Chief-of-staff persona | Momo |
| Sub-agent mechanism | 10 `delegate_task` specialists (leaf role, isolated context) + separate wildlife-caption profile worker; Kanban for durable profile-assigned tasks |
| LLM Provider | Nous; main `openai/gpt-6-luna`; wildlifephoto uses `openai/gpt-5.4-mini`; explicit cron/profile/auxiliary overrides |
| Memory | OpenViking (semantic KB, 127.0.0.1:1933) + Hermes always-on memory |
| Scheduling | Hermes Cron (built-in), script-only watchdog mode |
| Profiles | default + 11 specialist profiles |
| Platforms | Discord, WhatsApp (wa-bridge), Telegram (→Discord), Photon (iMessage) |
| Location | OwnTracks + mosquitto MQTT (TLS, password auth) |
| Trading | Zerodha Kite MCP (+ yfinance fallback), IBKR MCP, Minitrader |
| Remote ops | Mac Mini over Tailscale (SSH, AppleScript, CDP) |
| Hosting | Linux VPS (Hostinger) |
| Skill Count | 129 enabled shared skills across 53 registry categories |

## Scalability Profile

### Current Setup (Single User, Production)
- Runs autonomously on VPS + Mac - no single point of dependency
- 35 enabled cron jobs (39 registered); 10 `delegate_task` specialists plus 1 dedicated wildlife-photo profile worker; Kanban dispatcher enabled
- All platforms connected simultaneously
- OpenViking KB holds long-term memory; watchdog monitors its health

### What This Demonstrates
- Chief-of-staff + sub-agent orchestration at personal scale
- Reliable long-running automation, including script-only watchdogs
- Cross-platform message routing with region-specific delivery configuration
- Self-hosted production infra (MQTT location, wa-bridge, Tailscale Mac access)
- Composable skill architecture (129 enabled shared skills across 53 registry categories)
- Security-conscious configuration

---

*Architecture reviewed November 2026 (Hermes Agent v0.23.2)*
