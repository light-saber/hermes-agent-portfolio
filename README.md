# Hermes Agent Portfolio

A personal AI assistant agent system built with Hermes Agent, showcasing 89 specialized skills across 33 categories, 14 active automated workflows, a 6-specialist sub-agent roster, and deep multi-platform integration.

## What This Is

A production-grade personal AI agent system — not a demo, not a toy. It's built to run reliably every day: doing financial analysis, monitoring the AI ecosystem, managing email, watching deadlines, handling research tasks, and more. Momo is the chief-of-staff orchestrator; six specialist sub-agents do the deep work.

## At a Glance

| Dimension | Detail |
|-----------|--------|
| **Skills** | 89 across 33 categories |
| **Active Cron Jobs** | 14 (daily/weekly/monthly/one-shot) |
| **Sub-agents** | 6 specialists dispatched via `delegate_task` |
| **Profiles** | `default`, `tax-assist`, `hsbc-credit-card-manager` |
| **Platforms** | Discord, Telegram, Photon (iMessage) |
| **LLM Providers** | Anthropic, OpenAI Codex, MiniMax (MiniMax-M3) |
| **Hosting** | Linux VPS (Hostinger) |
| **Memory** | OpenViking (semantic KB) + Hermes memory (always-on) |

## Core Capabilities

### 🤖 Sub-agent Roster (chief-of-staff model)
Momo is the orchestrator. For non-trivial work, Momo dispatches to one of six specialist sub-agents via `delegate_task`. Each agent works in an isolated context and returns a clean summary.

| # | Agent | Domain | Skills loaded |
|---|-------|--------|---------------|
| 1 | **StockMan** | Ad-hoc equity research, "should I buy X", thesis reviews, sector deep-dives | `stockman`, `stock-prediction-model` |
| 2 | **TaxBuddy** | Form16/26AS/AIS reconciliation, capital gains, ITR-2 prep (lives in profile `tax-assist`) | `india-rsu-tax-filing` |
| 3 | **HomeBase** | Property escalations (apartments, builders), home loan amortization tracking, society dues, property decisions; watchdog duty | none typically |
| 4 | **HealthGuard** | Health insurance policy queries, claim filing, wearable health trend interpretation, family vaccination schedules | `ultrahuman-insights` |
| 5 | **CodeForge** | Side-project scoping — takes a 1-line idea, returns a Claude Code handoff brief (scope/README/milestones) | `github-pr-workflow` |
| 6 | **Researcher** | Deep dives (vaccines, tech comparisons, policy research) | `linkup-research`, `arxiv`, `blogwatcher` |

Default behavior: any multi-step or research-heavy ask → dispatch to the matching agent. Momo handles simple Q&A, single tool calls, and cron-managed workflows inline. The dispatch playbook lives in the `sub-agent-dispatch` skill.

### 🤖 Autonomous AI Agents (long-running)
Multi-agent orchestration with explicit stage-gating between planning and execution. Ideation and strategy live with Momo; execution is delegated to specialized coding agents (Claude Code, Codex, OpenCode) only after human approval.

### 📈 Financial Analysis (StockMan)
A dedicated financial analyst persona — runs every trading day:
- **9:00am IST** — Portfolio prediction for the day
- **3:45pm IST** — Compare prediction vs actual, log accuracy
- **Monthly** — Piotroski F-Score screener across NSE/US markets
- Tracks a diversified portfolio across gold, silver, sovereign bonds, banking, NBFC, metals, power, defense, fertilizers, autos, pharma, FMCG, logistics, and IT (full holdings stored privately — not committed to this repo)

### 📰 AI Ecosystem Monitoring
Daily 7am IST brief covering AI trends, OSS momentum, and developer tooling.

### 🏠 HomeBase (watchdog duties)
HomeBase runs as a daily watchdog cron at 10am IST — checks open property escalations (e.g., delayed builder handovers with hard deadlines) and alerts when deadlines approach. Case files under `~/.hermes/cases/homebase/`.

### 🎨 Creative & Media
ASCII art/video, infographics, architecture diagrams, HTML mockups, p5.js sketches, Manim math animations, ComfyUI image/video generation, design system implementations, Excalidraw diagrams.

### 📧 Productivity & Automation
Email (IMAP/SMTP), Google Workspace, Notion, Airtable, Microsoft Teams meetings, PDF OCR/editing, PowerPoint automation, Maps/routing.

### 🔬 MLOps & Research
Local LLM inference (llama.cpp, vLLM), HuggingFace model management, model benchmarking (lm-eval-harness), arXiv paper search, Polymarket prediction markets, flight/weather research.

### 🏠 Smart Home & Personal
Philips Hue lighting, Apple Reminders, Ultrahuman Ring health data, Yuanbao group management.

## Skills Overview

| Category | Count | Highlights |
|----------|-------|------------|
| autonomous-ai-agents | 9 | Claude Code, Codex, OpenCode, kanban, gbrain, hermes-gateway-ops |
| apple | 1 | macOS automation bundle |
| apple-reminders | 1 | Reminders via `remindctl` |
| computer-use | 1 | Drive the desktop in the background |
| creative | 3 | ComfyUI, design-md, ASCII art |
| data-science | 1 | Jupyter live kernel |
| devops | 2 | Kanban orchestrator/worker |
| dogfood | 1 | Exploratory QA of web apps |
| email | 2 | Himalaya CLI, thread search |
| financial-analysis | 3 | StockMan, India RSU tax, HSBC card |
| github | 6 | PR lifecycle, code review, repo mgmt, codebase inspection |
| hermes-agent-playbook | 1 | Scenario-specific Hermes workflows |
| hermes-desktop-plugins | 1 | Desktop plugin authoring |
| indian-bank-expense-digest | 1 | Daily digest from Indian bank alerts |
| linkup-extract | 1 | Structured extraction from a listing |
| linkup-fetch | 1 | Fetch a known URL's content |
| linkup-research | 1 | Exhaustive Linkup research |
| linkup-search | 1 | Default web lookup |
| linkup-workflow | 1 | Business-goal routing |
| media | 4 | GIF search, song generation, songsee, YouTube |
| mlops | 4 | llama.cpp, vLLM, HuggingFace, evaluation |
| note-taking | 1 | Obsidian |
| productivity | 11 | Email, Notion, PowerPoint, Teams, markitdown, maps, petdex, etc. |
| red-teaming | 1 | Jailbreak techniques |
| reference | 1 | Hermes Bible community resource |
| research | 8 | arXiv, blogwatcher, flights, polymarket, LLM wiki, etc. |
| smart-home | 1 | OpenHue |
| social-media | 3 | X/Twitter via xurl, Discord posting, xurl MCP |
| software-development | 8 | TDD, debugging, code review, spike, plan, VPS webpage |
| stock-prediction-model | 1 | Sachin's portfolio prediction model |
| sub-agent-dispatch | 1 | 6-specialist dispatch playbook |
| ultrahuman-insights | 1 | Ultrahuman ring data analysis |
| yuanbao | 1 | Yuanbao groups |

See [SKILLS.md](SKILLS.md) for the full skill inventory.

## Active Cron Jobs (14)

| Job | Schedule | Purpose | Delivery |
|-----|----------|---------|----------|
| Daily AI Ecosystem Brief | 7:00am IST | AI trends, OSS momentum, dev tools | Discord Home |
| Daily Ultrahuman Insights | 7:00am IST | Sleep, HRV, recovery insights | origin |
| Daily Morning Prediction | 9:00am IST (Mon–Fri) | StockMan portfolio prediction | origin |
| Daily Prediction vs Actual | 3:45pm IST (Mon–Fri) | Compare and log accuracy | origin |
| Daily WMT Stock Price | 6:00am IST (Mon–Fri) | Walmart Inc. price tracking | Discord |
| Daily memes (8:30am IST) | 8:30am IST | Daily GIF delivery | Discord |
| MailScout | 2:30pm IST | Expense tracking from bank email alerts | Discord |
| Monthly Stock Screener | 1st of month, 9am IST | Piotroski F-Score NSE+US | origin |
| Enhanced Screener — NSE Monthly | 1st of month, 3:30am UTC | Enhanced screener digest | Discord |
| HSBC Premier Monthly Brief | 1st of month, midnight UTC | Credit card spend brief | Discord |
| HomeBase property watchdog | 10:00am IST | Open-escalation deadline monitor (HomeBase sub-agent) | Discord |
| Kimi subscription + cron migration | 18 Aug 2026 09:00 IST | One-shot reminder | origin |
| Kimi signup backup reminder | 15 Aug 2026 09:00 IST | One-shot backup reminder | origin |
| WhatsApp response monitor | every 60m | Paused/disabled | origin |

## Architecture

The system has four main layers, plus a sub-agent dispatch layer:

```
┌──────────────────────────────────────────────────────┐
│                    Platforms                         │
│         Discord · Telegram · Photon (iMessage)       │
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
  │  6 Sub-  │    │  Skill System │    │  Memory Layer    │
  │  agents  │    │  88 skills    │    │  Hermes + Open   │
  │ delegate │    │  28 cats      │    │  Viking          │
  │  _task   │    └──────────────┘    └──────────────────┘
  └──────────┘
        │
        ├─▶ StockMan / TaxBuddy / HomeBase / HealthGuard /
        │   CodeForge / Researcher
        │
┌───────▼───────────────────────────────────────────┐
│        Cron Scheduler + MCP Tools                  │
│  14 active jobs · Kite · GitHub · Discord · Hue    │
└───────────────────────────────────────────────────┘
```

See [docs/architecture.md](docs/architecture.md) for the full technical architecture.

## Platform Integrations

| Platform | What's Connected |
|----------|------------------|
| **Discord** | Primary home channel, Ideas channel for AI briefs, StockMan output, all cron deliveries (Telegram deliveries are routed here since Telegram is banned in India) |
| **Telegram** | Connected at the API layer; deliveries fan out to Discord Home for cron jobs |
| **Photon** | iMessage integration for mobile |
| **GitHub** | PR workflow, code review, repo management |
| **Kite (Zerodha)** | Real-time prices, order management, portfolio (NSE/BSE only; US via yfinance) |
| **Discord (admin)** | Channel/role management, member search, message pinning, thread creation |
| **Discord** | Message send/reply/react via bot |
| **Google Workspace** | Gmail, Calendar, Drive, Docs |
| **Notion** | Knowledge base and notes |
| **Airtable** | Structured data operations |
| **Philips Hue** | Smart lighting |
| **Ultrahuman Ring** | Health data via Apple Health |

## Configuration Templates

Sample configurations are in `config/templates/`:

```bash
# Template is markdown; copy as a starting point and rename to .yaml
cp config/templates/config.example.md config/config.yaml
# Edit with your API keys and preferences
```

## Profiles (persistent contexts)

- `default` — main Momo profile (current).
- `tax-assist` — sustained ITR work; carries tax workspace and documents across sessions.
- `hsbc-credit-card-manager` — credit card statement analysis and rewards optimization.

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

See [docs/setup.md](docs/setup.md) for the full setup guide.

## What I Learned

Building this system taught me:
- Chief-of-staff orchestration with sub-agent dispatch (sub-agents keep context windows lean)
- Multi-agent orchestration with explicit stage gates
- Tool calling and API integration at scale
- Reliable scheduled task execution with multi-platform delivery
- Platform-specific bot development nuances
- Security best practices (env vars, no secrets in files)
- System architecture for composable, maintainable agent systems

## License

MIT License — feel free to use as inspiration for your own projects.

---

*Built with Hermes Agent by Nous Research. Last updated July 2026.*