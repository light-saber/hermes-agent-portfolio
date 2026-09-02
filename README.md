# Hermes Agent Portfolio

A personal AI assistant agent system built with Hermes Agent, showcasing 150+ specialized skills across 53 categories, a 10-specialist sub-agent roster (each a real Hermes profile), ~30 active automated workflows, and deep multi-platform integration.

## What This Is

A production-grade personal AI agent system — not a demo, not a toy. It's built to run reliably every day: doing financial analysis, monitoring the AI ecosystem, managing email and WhatsApp group ops, tracking health and family milestones, watching deadlines, and handling research. **Momo** is the chief-of-staff orchestrator; ten specialist sub-agents do the deep work — each one living as its own Hermes profile so it's visible in the desktop **Bots** tab.

## At a Glance

| Dimension | Detail |
|-----------|--------|
| **Skills** | ~150 across 53 categories (active; archived/pruned excluded) |
| **Cron Jobs** | ~30 active (38 registered; recurring + one-shot) |
| **Sub-agents** | 10 specialists dispatched via `delegate_task` |
| **Profiles** | `default` + 10 specialist profiles (each sub-agent is a Bot) |
| **Platforms** | Discord, WhatsApp (wa-bridge), Telegram, Photon (iMessage), Mac (MacPilot) |
| **Location** | OwnTracks GPS pipeline (self-hosted MQTT broker on VPS) |
| **LLM Provider** | Alibaba (DeepSeek V4 Flash via DashScope); Nous for image gen / aux vision |
| **Hosting** | Linux VPS (Hostinger) + Mac Mini (Tailscale remote access) |
| **Memory** | OpenViking (semantic KB) + Hermes always-on memory |

## Core Capabilities

### 🤖 Sub-agent Roster (chief-of-staff model)

Momo is the orchestrator. For non-trivial work, Momo dispatches to a specialist sub-agent via `delegate_task` — each works in an isolated context and returns a clean summary. Each specialist also runs as a real Hermes profile (a desktop Bot) with its own SOUL.md persona. The dispatch playbook, personalities, and guardrails live in the `agent-orchestration`, `sub-agent-personalities`, and `sub-agent-guardrails` skills.

| # | Agent | Domain | Profile / skills |
|---|-------|--------|------------------|
| 1 | **MacPilot** | Drives the user's Mac — Safari, files, screenshots, macOS shell (SSH + AppleScript + CDP over Tailscale) | `macpilot`, `computer-use`, `tailscale-mac-remote-access` |
| 2 | **StockMan** | Ad-hoc equity research, "should I buy X", thesis reviews, sector deep-dives, daily portfolio prediction | `stockman`, `stock-prediction-model` |
| 3 | **TaxBuddy** | Form16/26AS/AIS reconciliation, capital gains, ITR-2 prep & advance-tax | `tax-assist` profile, `india-rsu-tax-filing` |
| 4 | **HomeBase** | Property escalations (builders, society), home loan amortization, watchdog duty | `homebase` profile, case files under `~/.hermes/cases/homebase/` |
| 5 | **HealthGuard** | Health insurance policy queries, claim filing, wearable health trends, family vaccinations | `healthguard` profile, `ultrahuman-insights` |
| 6 | **FamilyDoc** | Family physician triage — symptoms, Rx, vaccine info, working "AI diagnosis" labels (lives in #life-tracker) | `familydoc`, `pregnancy-milestone-tracker` |
| 7 | **CodeForge** | Side-project scoping — 1-line idea → Claude Code handoff brief (never writes code) | `codeforge` profile, `github-pr-workflow` |
| 8 | **Researcher** | Multi-source deep dives with citations | `researcher`, `linkup-research`, `arxiv`, `blogwatcher` |
| 9 | **QABot** | QA after every CodeForge build — evidence-led verdicts, dogfood browser testing | `qabot`, `dogfood`, `github-pr-workflow` |
| 10 | **HSBC Card Manager** | HSBC Premier credit card statement analysis & rewards optimization | `hsbc-credit-card-manager`, `hsbc-credit-card-manager` skill |

Default behavior: any multi-step or research-heavy ask → dispatch to the matching agent. Momo handles simple Q&A, single tool calls, and cron-managed workflows inline.

### 🤖 Autonomous AI Agents (long-running + handoff)
Multi-agent orchestration with explicit stage-gating between planning and execution. Ideation and strategy live with Momo; execution is delegated to specialized coding agents (Claude Code, Codex, OpenCode) only after an explicit user handoff signal. CodeForge scopes, QABot verifies, Claude Code builds — each phase is a separate gated step.

### 📈 Financial Analysis (StockMan + Minitrader)
A dedicated financial-analysis stack that runs every trading day:
- **9:00am IST** — portfolio prediction for the day (stock-prediction-model)
- **3:45pm IST** — compare prediction vs actual, log accuracy
- **Portfolio activity watchdog** — low-noise price/volume anomaly alerts (NSE intraday, NSE close, WMT close)
- **Minitrader** — dual long-term portfolio (live + paper) on Zerodha Kite, CNC-only, human-in-the-loop buy gate, Nifty50 benchmark
- **IBKR tracker** — daily Interactive Brokers portfolio snapshot
- **Monthly** — Piotroski F-Score + quality/momentum screeners with forward-view analyst/news corroboration, across NSE/US
- Holdings and positions stored privately — never committed to this repo

### 📰 AI Ecosystem Monitoring
Daily brief (7:00am IST) covering AI trends, OSS momentum, and developer tooling, plus a daily AI newsletter email (delivered to inbox).

### 🏠 HomeBase (watchdog duties)
Daily watchdog cron — checks open property escalations (e.g., delayed builder handovers with hard deadlines) and alerts when deadlines approach. Case files live under `~/.hermes/cases/homebase/` and are keyed by deliverable, not just case state (alerts are idempotent by case+trigger+deadline+state).

### 💬 Messaging & Location
- **WhatsApp** — VPS `wa-bridge` (:8765) for reading and sending. Cron nudges to the "tiffin pe charcha" group (Friday cab-booking nudge, lunch asks); breakfast/lunch asks gated on office arrival via OwnTracks.
- **Location** — self-hosted OwnTracks + MQTT (mosquitto, Let's Encrypt TLS, password auth) on the VPS. Replaces impossible Google/Apple location APIs; reverse-geocodes phone fixes to addresses, drives office-presence automations.
- **iMessage / Photon** and **Telegram** (banned in India — deliveries fan out to Discord #general).

### 🏥 Family & Health
FamilyDoc triages symptoms (every diagnosis tagged "AI diagnosis"); HealthGuard owns insurance/claims/vaccines; a **pregnancy milestone tracker** schedules NT/anomaly/GTT/Tdap/term reminders; Ultrahuman ring data syncs and delivers insights daily.

### 🎨 Creative & Media
Image/video generation, infographics/architecture diagrams, ASCII art/video, GIF sourcing, song generation (HeartMuLa), audio spectrograms, meme sourcing, YouTube transcripts.

### 📧 Productivity & Automation
Email (IMAP/SMTP via Himalaya, expense digest, subscription audit), Google Workspace, Notion, document conversion (markitdown, OCR, PDF, PPTX, XLSX), Maps/routing, hospital portal booking.

### 🔬 MLOps & Research
Local LLM inference (llama.cpp, vLLM), HuggingFace model management, benchmark harness, arXiv, Polymarket, flights, Reddit read-only, grounded citations.

## Skills Overview

See [SKILLS.md](SKILLS.md) for the full inventory — **150 active skills across 53 categories** (last-generation, archived skills excluded). Top categories by count: productivity (28), software-development (18), research (11), autonomous-ai-agents (10), financial-analysis (8), media (7), mlops (6).

## Active Cron Jobs (~30)

| Job | Schedule | Purpose | Delivery |
|-----|----------|---------|----------|
| Daily AI Ecosystem Brief | 7:00am IST | AI trends, OSS momentum, dev tools | Discord #home |
| Daily AI Newsletter Email | 8:00am IST | Same brief as HTML email digest | inbox |
| Daily WMT Stock Price | 6:00am IST (Mon–Fri) | Walmart price tracking | Discord |
| Ultrahuman sync + insights | 6:30am IST | Ring data sync, delivers only when noteworthy | Discord |
| Morning Prediction | 9:00am IST (Mon–Fri) | StockMan portfolio forecast | origin |
| Prediction vs Actual | 3:45pm IST (Mon–Fri) | Compare + log accuracy | origin |
| MailScout expense digest | 2:30pm IST | Bank-email expense tracking (dedupes card-bill repayments vs consumption) | origin |
| HomeBase property watchdog | 10:00am IST | Open-escalation deadline monitor | Discord |
| Portfolio watchdog — NSE intraday | every 30m | Price/volume anomaly scan | Discord |
| Portfolio watchdog — NSE close | 3:45pm IST (Mon–Fri) | EOD anomaly digest | Discord |
| Portfolio watchdog — WMT close | 9:45pm IST (Mon–Fri) | US EOD anomaly digest | Discord |
| IBKR portfolio tracker | 9:30pm IST (Mon–Fri) | Daily IBKR holdings snapshot | Discord |
| Minitrader paper pick | 9:30am IST (Mon–Fri) | Paper-portfolio build pick | Discord |
| Pregnancy week check-in | 9:00pm IST Sun | Gestational week nudge | Discord |
| NT scan booking reminder | 9:00am IST (one-shot) | Pre-NT-scan booking nudge | origin |
| Advance tax reminders | Sep/TAR-quarterly | Q2 top-up (~₹14K by Sep 15), quarterly 234C check | origin |
| Track Hermes clarify PRs | every 6h | Watch upstream Hermes PRs | origin |
| Alisha Friday cab nudge | 9:00am IST Fri | WhatsApp group nudge | origin |
| Office arrival lunch/breakfast asks | wkdays, gated by OwnTracks | Breakfast/lunch WhatsApp pokes | local |
| Monthly stock screeners | 1st of month | Piotroski + quality/momentum + forward view, NSE+US | origin |
| HSBC Premier Monthly Brief | 1st of month | Credit card spend brief | Discord |
| Subscription audit | 1st of month, 10am | Recurring-spend audit from email | Discord |
| Memory-system watchdog | every 6h | OpenViking backend health | Discord |
| Pregnancy milestone one-shots | NT/anomaly/GTT/Tdap/term | Scan-window reminders | Discord |

Plus several completed one-shot jobs (cough follow-up, tax reminders, nameplate nudges). Paused: daily memes, Minitrader live pick.

## Architecture

The system has four main layers, plus a sub-agent dispatch layer:

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
  │10 Sub-   │    │  Skill System │    │  Memory Layer    │
  │ agents   │    │  150 skills   │    │  Hermes + Open   │
  │(delegate)│    │  53 cats      │    │  Viking          │
  └──────────┘    └──────────────┘    └──────────────────┘
        │
        ├─▶ MacPilot / StockMan / TaxBuddy / HomeBase /
        │   HealthGuard / FamilyDoc / CodeForge /
        │   Researcher / QABot / HSBC Card Manager
        │
┌───────▼───────────────────────────────────────────┐
│        Cron Scheduler + MCP + External Ops         │
│  ~30 jobs · Kite · IBKR · GitHub · Discord · Hue   │
│  WhatsApp wa-bridge · OwnTracks MQTT · Mac SSH     │
└───────────────────────────────────────────────────┘
```

See [docs/architecture.md](docs/architecture.md) for the full technical architecture.

## Platform Integrations

| Platform | What's Connected |
|----------|------------------|
| **Discord** | Primary home channel, all cron deliveries, sub-bot outputs per channel |
| **WhatsApp** | VPS wa-bridge (:8765) — read + send; group nudges, office-presence asks |
| **Telegram** | Connected at API layer; deliveries fan out to Discord (banned in India) |
| **Photon (iMessage)** | Mobile-first channel |
| **OwnTracks** | Self-hosted MQTT location broker → GPS pipeline |
| **Mac (MacPilot)** | Full desktop control over Tailscale (SSH + AppleScript + CDP) |
| **GitHub** | PR workflow, code review, repo management |
| **Kite (Zerodha)** | Trading, holdings, GTT (NSE/BSE; US via yfinance fallback) |
| **IBKR** | Daily portfolio snapshot via Claude Code CLI + IBKR MCP |
| **Mail** | Gmail via Himalaya IMAP/SMTP + Google Workspace |

## Configuration Templates

Sample configurations are in `config/templates/` (`config.example.md` — copy, rename to `.yaml`, fill in keys):

```bash
cp config/templates/config.example.md config/config.yaml
```

## Profiles (persistent contexts — each is a desktop Bot)

Every specialist is a real `~/.hermes/profiles/<name>/` profile with its own SOUL.md persona + profile.yaml:

- `default` — main Momo profile (orchestrator, current).
- `stockman`, `homebase`, `healthguard`, `familydoc`, `codeforge`, `researcher`, `qabot`, `macpilot` — specialist Bots.
- `tax-assist` — sustained ITR work; TaxBuddy's profile.
- `hsbc-credit-card-manager` — credit card statement analysis and rewards.

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
2. Copy `config/templates/config.example.md` to `config.yaml`
3. Add your API keys
4. Load skills as needed

## What I Learned

Building this system taught me:
- Chief-of-staff orchestration with sub-agent dispatch (sub-agents keep context windows lean)
- The cron-can't-delegate gotcha: cron prompts are self-contained orchestrators, not dispatchers
- Multi-agent orchestration with explicit stage gates (plan → Claude Code → QA)
- Reliable scheduled task execution with multi-platform delivery and state-gated watchdogs
- Self-hosting real infra: OwnTracks MQTT + TLS, VPS wa-bridge, Tailscale Mac access
- Platform-specific bot development nuances
- Security best practices (env vars, no secrets in files — case files and holdings never committed)

## License

MIT License — feel free to use as inspiration for your own projects.

---

*Built with Hermes Agent by Nous Research. Last updated August 2026.*