# Hermes Agent Portfolio

A personal AI assistant agent system built with Hermes Agent v0.23.2, showcasing 129 enabled shared skills across 53 registry categories, 11 specialist profiles, 35 enabled scheduled workflows (39 registered), and deep multi-platform integration.

## What This Is

A production-grade personal AI agent system - not a demo, not a toy. It's built to run reliably every day: doing financial analysis, monitoring the AI ecosystem, managing email and WhatsApp group ops, tracking health and family milestones, watching deadlines, and handling research. **Momo** is the chief-of-staff orchestrator. Ten specialists are dispatched through Hermes `delegate_task`; a separate wildlife-photo specialist runs in its own profile for image-grounded caption drafting. The specialist profiles are visible in the desktop **Bots** tab.

## At a Glance

| Dimension | Detail |
|-----------|--------|
| **Skills** | 129 enabled shared skills across 53 registry categories (profile-local and disabled skills excluded) |
| **Cron Jobs** | 35 enabled (39 registered; 4 disabled) |
| **Sub-agents** | 10 specialists dispatched via `delegate_task`, plus 1 dedicated wildlife-caption profile |
| **Profiles** | `default` + 11 specialist profiles |
| **Platforms** | Discord, WhatsApp (wa-bridge), Telegram, Photon (iMessage), Mac (MacPilot) |
| **Location** | OwnTracks GPS pipeline (self-hosted MQTT broker on VPS) |
| **LLM Provider** | Nous; main model `openai/gpt-6-luna`; wildlife-caption profile uses `openai/gpt-5.4-mini`; explicit cron overrides |
| **Durable Work Queue** | Hermes Kanban dispatcher enabled; separate from bounded `delegate_task` calls |
| **Hosting** | Linux VPS (Hostinger) + Mac Mini (Tailscale remote access) |
| **Memory** | OpenViking (semantic KB) + Hermes always-on memory |

## Core Capabilities

### 🤖 Specialist Roster (chief-of-staff model)

Momo is the orchestrator. For non-trivial work, Momo dispatches to one of ten specialist sub-agents via `delegate_task` - each works in an isolated context and returns a clean summary. A separate wildlife-caption worker uses its dedicated Hermes profile. Specialist profiles also have their own personas and are visible in the desktop Bots view. The dispatch playbook, personalities, and guardrails live in the `agent-orchestration`, `sub-agent-personalities`, and `sub-agent-guardrails` skills. See [specialist routing](docs/specialists.md) for how the profile-based caption worker differs from a `delegate_task` child.

| # | Agent | Domain | Profile / skills |
|---|-------|--------|------------------|
| 1 | **MacPilot** | Drives the user's Mac - Safari, files, screenshots, macOS shell (SSH + AppleScript + CDP over Tailscale) | `macpilot`, `browser-skill`, `tailscale-mac-remote-access` |
| 2 | **StockMan** | Ad-hoc equity research, "should I buy X", thesis reviews, sector deep-dives, daily portfolio prediction | `stockman`, `stock-prediction-model` |
| 3 | **TaxBuddy** | Form16/26AS/AIS reconciliation, capital gains, ITR-2 prep & advance-tax | `tax-assist` profile, `india-rsu-tax-filing` |
| 4 | **HomeBase** | Property escalations (builders, society), home loan amortization, watchdog duty | `homebase` profile |
| 5 | **HealthGuard** | Health insurance policy queries, claim filing, and wearable health trends | `healthguard` profile, `ultrahuman-insights` |
| 6 | **FamilyDoc** | Family health information and triage, with appropriate clinical limits | `familydoc` profile + skill |
| 7 | **CodeForge** | Side-project scoping - 1-line idea → Claude Code handoff brief (never writes code) | `codeforge` profile, `github-pr-workflow` |
| 8 | **Researcher** | Multi-source deep dives with citations | `researcher`, `linkup`, `arxiv`, `blogwatcher` |
| 9 | **QABot** | QA after every CodeForge build - evidence-led verdicts, dogfood browser testing | `qabot`, `dogfood`, `github-pr-workflow` |
| 10 | **HSBC Card Manager** | HSBC Premier credit card statement analysis & rewards optimization | `hsbc-credit-card-manager` profile + skill |
| 11 | **Feather / WildlifePhoto** | Wildlife-photo caption drafting from image observations and verified EXIF; draft-only, never publishes | `wildlifephoto` profile; dedicated caption worker (not a `delegate_task` agent) |

Default behavior: any multi-step or research-heavy ask → dispatch to the matching agent. Wildlife-photo captions use the dedicated `wildlifephoto` profile worker rather than `delegate_task`. Longer-lived profile-assigned work can use the separately configured Kanban dispatcher. Momo handles simple Q&A, single tool calls, and cron-managed workflows inline.

### 🤖 Autonomous AI Agents (long-running + handoff)
Multi-agent orchestration with explicit stage-gating between planning and execution. Ideation and strategy live with Momo; execution is delegated to specialized coding agents (Claude Code, Codex, OpenCode) only after an explicit user handoff signal. CodeForge scopes, QABot verifies, Claude Code builds - each phase is a separate gated step.

### 📈 Financial Analysis (StockMan + Minitrader)
A dedicated financial-analysis stack that runs every trading day:
- **9:00am IST** - portfolio prediction for the day (stock-prediction-model)
- **3:45pm IST** - compare prediction vs actual, log accuracy
- **Portfolio activity watchdog** - low-noise price/volume anomaly alerts (NSE intraday, NSE close, WMT close)
- **Minitrader** - dual long-term portfolio (live + paper) on Zerodha Kite, CNC-only, human-in-the-loop buy gate, Nifty50 benchmark
- **Vested tracker** - weekday US portfolio snapshot
- **Monthly** - Piotroski F-Score + quality/momentum screeners with forward-view analyst/news corroboration, across NSE/US
- Holdings and positions stored privately - never committed to this repo

### 📰 AI Ecosystem Monitoring
Unified morning digest (8:15am IST) covering AI trends, OSS momentum, and developer tooling, with delivery across Discord, email, and WhatsApp.

### 🏠 HomeBase
HomeBase handles property escalations and tracks deliverable-owned deadlines. Private case files are keyed by deliverable, not just case state; alerts are idempotent by case, trigger, deadline, and state.

### 💬 Messaging & Location
- **WhatsApp** - a self-hosted bridge for reading and sending. Group nudges are workflow-gated; office-arrival breakfast/lunch nudges are currently paused.
- **Location** - self-hosted OwnTracks + MQTT (mosquitto, Let's Encrypt TLS, password auth) on the VPS. Replaces impossible Google/Apple location APIs; reverse-geocodes phone fixes to addresses, drives office-presence automations.
- **iMessage / Photon** and **Telegram** scheduled deliveries are routed to Discord.

### 🏥 Family & Health
FamilyDoc handles health information and triage with appropriate clinical limits; HealthGuard covers insurance, claims, and wearable trends; family-care reminders are kept generic in this public overview. Ultrahuman ring data syncs and delivers insights daily.

### 🛒 Shopping & Smart Home
Amazon ordering through the Mac over CDP (including re-adding past purchases), a Swiggy/Zepto grocery dual-cart layer, and smart-home integrations: MG ZS EV telemetry (charge reminders, drive logging), Philips Hue via OpenHue, and appliance guides (microwave, tumble dryer).

### 🎨 Creative & Media
Image/video generation, infographics/architecture diagrams, ASCII art/video, GIF sourcing, song generation (HeartMuLa), audio spectrograms, meme sourcing, YouTube transcripts.

### 📧 Productivity & Automation
Email (IMAP/SMTP via Himalaya, expense digest, subscription audit), Google Workspace, Notion, document conversion (markitdown, OCR, PDF, PPTX, XLSX), Maps/routing, hospital portal booking.

### 🔬 MLOps & Research
Local LLM inference (llama.cpp, vLLM), HuggingFace model management, benchmark harness, arXiv, Polymarket, flights, Reddit read-only, grounded citations.

## Skills Overview

See [SKILLS.md](SKILLS.md) for the full inventory - **129 enabled shared skills across 53 registry categories** (disabled and profile-local skills excluded). Largest categories include productivity (17), software-development (12), research (11), financial-analysis (9), autonomous-ai-agents (8), and smart-home (6).

## Selected Scheduled Workflows (35 enabled; 39 registered)

| Job | Schedule | Purpose | Delivery |
|-----|----------|---------|----------|
| Unified Morning Digest (Email + WhatsApp + Discord) | 8:15am IST | Consolidated daily digest | Discord + email + WhatsApp |
| Daily WMT Stock Price | 6:00am IST (Mon-Fri) | Walmart price tracking | Discord |
| Ultrahuman sync + insights | 6:30am IST | Ring data sync, delivers only when noteworthy | Discord |
| Morning Prediction | 9:00am IST (Mon-Fri) | StockMan portfolio forecast | origin |
| Prediction vs Actual | 3:45pm IST (Mon-Fri) | Compare + log accuracy | origin |
| MailScout expense digest | 2:30pm IST | Bank-email expense tracking (dedupes card-bill repayments vs consumption) | origin |
| Family-care week change notification | 9:00am IST Mon | Weekly check-in | origin |
| Combined Quality + Momentum Screener | 1st of month, 11am | NSE/US screen | origin |
| Portfolio watchdog - NSE intraday | every 30m | Price/volume anomaly scan | Discord |
| Portfolio watchdog - NSE close | 3:45pm IST (Mon-Fri) | EOD anomaly digest | Discord |
| Portfolio watchdog - WMT close | 9:45pm IST (Mon-Fri) | US EOD anomaly digest | Discord |
| Vested US Portfolio Daily Tracker | 9:00am IST (Mon-Fri) | Script-only US portfolio snapshot | configured delivery |
| Family-care week check-in | Weekly | Family milestone nudges | Discord |
| Family-care milestone one-shots | Scheduled windows | Health and care reminders | Discord |
| Advance tax checks + reminders | Jun/Sep/Dec + one-shots | Quarterly checks and Q3 payment/deadline reminders | origin |
| Long-term financial reminder | One-shot | Scheduled financial follow-up | origin |
| Track Hermes clarify PRs | every 6h | Watch upstream Hermes PRs | origin |
| Friday cab-booking nudge | 9:00am IST Fri | WhatsApp group nudge | origin |
| Daily WhatsApp pop quiz | 10:00am IST | Group quiz | local |
| Office-arrival breakfast/lunch asks | Paused; OwnTracks-gated scripts | Not currently sending | local |
| MG EV charge reminder | 9am / 8pm IST | Low-range charge nudge from EV telemetry | origin |
| Commute tracker + notify | every 2m / webhook | Home/office transition detection; phone notify on change | local / Photon |
| Monthly stock screeners | 1st of month | Piotroski + quality/momentum + forward view, NSE+US | origin |
| HSBC Premier Monthly Brief | 1st of month | Credit card spend brief | Discord |
| Subscription audit | 1st of month, 10am | Recurring-spend audit from email | Discord |
| Memory-system watchdog | every 6h | OpenViking backend health | Discord |

The registered total includes disabled workflows; one-shot and paused jobs may change over time. The live fleet also has additional one-shots and monitoring jobs not individually listed here. Cron sessions run self-contained prompts and do not call `delegate_task`.

## Architecture

The system has four main layers, plus specialist dispatch and durable Kanban work queues:

```
┌──────────────────────────────────────────────────────┐
│                    Platforms                         │
│   Discord · WhatsApp(wa-bridge) · Telegram(banned→   │
│   Discord) · Photon(iMessage) · OwnTracks GPS        │
└────────────────────────┬───────────────────────────┘
                         │
┌────────────────────────▼───────────────────────────┐
│               Momo (Chief of Staff)                 │
│      Routes requests · dispatches sub-agents        │
└────────────────────────┬───────────────────────────┘
                         │
        ┌────────────────┼──────────────────────┐
        ▼                ▼                      ▼
  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐
  │10 agents +  │    │Skill System │    │Memory Layer  │
  │1 profile    │    │129 skills   │    │Hermes + Open │
  │worker       │    │53 categories│    │Viking        │
  └──────────┘    └──────────────┘    └──────────────────┘
        │
        ├─▶ delegate_task: MacPilot / StockMan / TaxBuddy / HomeBase /
        │   HealthGuard / FamilyDoc / CodeForge / Researcher /
        │   QABot / HSBC Card Manager
        └─▶ photo-caption helper: Feather / WildlifePhoto profile
        │
┌───────▼───────────────────────────────────────────┐
│        Cron Scheduler + MCP + External Ops         │
│  35 enabled jobs · Kite · GitHub · Discord · Hue     │
│  WhatsApp wa-bridge · OwnTracks MQTT · Mac SSH     │
└───────────────────────────────────────────────────┘
```

See [docs/architecture.md](docs/architecture.md) for the full technical architecture.

## Platform Integrations

| Platform | What's Connected |
|----------|------------------|
| **Discord** | Primary home channel, all cron deliveries, sub-bot outputs per channel |
| **WhatsApp** | VPS wa-bridge - read + send; group nudges, office-presence workflows |
| **Telegram** | Connected at API layer; scheduled deliveries are routed to Discord |
| **Photon (iMessage)** | Mobile-first channel |
| **OwnTracks** | Self-hosted MQTT location broker → GPS pipeline |
| **Mac (MacPilot)** | Full desktop control over Tailscale (SSH + AppleScript + CDP) |
| **GitHub** | PR workflow, code review, repo management |
| **Kite (Zerodha)** | Trading, holdings, GTT (NSE/BSE; US via yfinance fallback) |
| **Mail** | Gmail via Himalaya IMAP/SMTP + Google Workspace |

## Configuration Reference

See [`config/templates/config.example.md`](config/templates/config.example.md) for a documented reference, not a drop-in runtime config. Live Hermes settings are stored in private user configuration and must not be published verbatim.

## Profiles (persistent contexts - specialist profiles are desktop Bots)

The ten `delegate_task` specialists have corresponding profile contexts; Feather is an additional profile-based caption worker:

- `default` - main Momo profile (orchestrator, current).
- `stockman`, `homebase`, `healthguard`, `familydoc`, `codeforge`, `researcher`, `qabot`, `macpilot` - specialist Bots.
- `tax-assist` - sustained ITR work; TaxBuddy's profile.
- `hsbc-credit-card-manager` - credit card statement analysis and rewards.
- `wildlifephoto` - Feather, dedicated wildlife-photo caption specialist. A helper passes vision observations and any actually extracted EXIF to this profile; it returns drafts only and never publishes.

The Kanban dispatcher is enabled for durable, profile-assigned work and is distinct from `delegate_task`, which is a bounded synchronous delegation mechanism. Curator is also enabled for lifecycle management of eligible agent-created skills; both features use the Hermes runtime rather than custom cron wrappers.

## Skills Structure

Each skill is a self-contained package:

```
skills/
└── category/
    └── skill-name/
        ├── SKILL.md           # Main skill definition
        ├── references/        # Supporting docs
        ├── templates/         # Config templates
        └── scripts/           # Helper scripts
```

## Setup

1. Install Hermes Agent
2. Run `hermes setup` and use `hermes config` to create a valid runtime configuration
3. Add credentials through supported environment/auth flows; never commit secrets
4. Configure profiles and skills for your own tool access and workflows

## What I Learned

Building this system taught me:
- Chief-of-staff orchestration with sub-agent dispatch (sub-agents keep context windows lean)
- The cron-can't-delegate gotcha: cron prompts are self-contained orchestrators, not dispatchers
- Multi-agent orchestration with explicit stage gates (plan → Claude Code → QA)
- Reliable scheduled task execution with multi-platform delivery and state-gated watchdogs
- Self-hosting real infra: OwnTracks MQTT + TLS, VPS wa-bridge, Tailscale Mac access
- Platform-specific bot development nuances
- Security best practices (env vars, no secrets in files - case files and holdings never committed)

## License

MIT License - feel free to use as inspiration for your own projects.

---

*Built with Hermes Agent by Nous Research. Last reviewed November 2026 (v0.23.2).*
