# Hermes Agent Portfolio

A personal AI assistant agent system built with Hermes Agent, showcasing 84 specialized skills across 20 categories, 7 active automated workflows, and deep multi-platform integration.

## What This Is

A production-grade personal AI agent system — not a demo, not a toy. It's built to run reliably every day: doing financial analysis, monitoring the AI ecosystem, managing email, handling research tasks, and more.

## At a Glance

| Dimension | Detail |
|-----------|--------|
| **Skills** | 84 across 20 categories |
| **Active Cron Jobs** | 7 (daily/weekly/monthly) |
| **Platforms** | Discord, Telegram, Photon (iMessage) |
| **LLM Providers** | Anthropic, OpenAI Codex, MiniMax |
| **Hosting** | Linux VPS (Hostinger) |
| **Memory** | OpenViking (semantic KB) + session context |

## Core Capabilities

### 🤖 Autonomous AI Agents
Multi-agent orchestration with explicit stage-gating between planning and execution. Ideation and strategy live with the main assistant; execution is delegated to specialized coding agents (Claude Code, Codex, OpenCode) only after human approval.

### 📈 Financial Analysis (StockMan)
A dedicated financial analyst persona — runs every trading day:
- **9:00am IST** — Portfolio prediction for the day
- **3:00pm IST** — Compare prediction vs actual, log accuracy
- **Monthly** — Piotroski F-Score screener across NSE/US markets
- Covers 24 holdings: GOLDBEES, SILVERBEES, SGBs, ICICIBANK, KOTAKBANK, MANAPPURAM, M&MFIN, SHRIRAMFIN, TATASTEEL, NATIONALUM, NMDC, POWERGRID, TATAPOWER, MTARTECH, COROMANDEL, HEROMOTOCO, LUPIN, ZYDUSLIFE, TATACONSUM, VOLTAS, DELHIVERY, TCS, RATEGAIN

### 📰 AI Ecosystem Monitoring
Daily 7am IST brief covering:
- AI trends worth paying attention to
- Open source projects gaining momentum
- New tools developers are adopting

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
| creative | 17 | ASCII art, infographics, design systems, p5.js, ComfyUI |
| autonomous-ai-agents | 6 | Claude Code, Codex, OpenCode, staged workflows |
| software-development | 9 | TDD, debugging, code review, spike workflows |
| productivity | 12 | Email, Notion, Airtable, PowerPoint, Teams |
| research | 8 | arXiv, blog RSS, Polymarket, flights |
| github | 6 | PR lifecycle, code review, repo management |
| mlops | 4 | llama.cpp, vLLM, HuggingFace, evaluation |
| apple | 5 | Reminders, desktop control |
| financial-analysis | 2 | StockMan analyst, India RSU tax |
| media | 4 | GIF search, song generation, YouTube |
| dogfood | 2 | Exploratory QA of web apps |
| devops | 2 | DevOps automation |

See [SKILLS.md](SKILLS.md) for the full skill inventory.

## Active Cron Jobs

| Job | Schedule | Purpose |
|-----|----------|---------|
| Daily AI Ecosystem Brief | 7:00am IST | AI trends, OSS momentum, dev tools |
| Daily Morning Prediction | 9:00am IST (Mon–Fri) | StockMan portfolio prediction |
| Daily Prediction vs Actual | 3:00pm IST (Mon–Fri) | Compare and log accuracy |
| Daily WMT Stock Price | 6:00am IST (Mon–Fri) | Walmart Inc. price tracking |
| Portfolio Prediction vs Actual | 3:00pm IST (Mon–Fri) | Portfolio-level comparison |
| Monthly Stock Screener | 1st of month, 9am IST | Piotroski F-Score screen |
| MailScout | 2:30pm IST daily | Expense tracking from email |

All jobs deliver to Discord (primary), with some also delivering to origin.

## Architecture

The system has four main layers:

```
┌──────────────────────────────────────────────────────┐
│                    Platforms                         │
│         Discord · Telegram · Photon (iMessage)       │
└────────────────────────┬───────────────────────────┘
                         │
┌────────────────────────▼───────────────────────────┐
│               Hermes Agent Core                     │
│   Skills · Memory · Cron Scheduler · MCP Tools        │
└────────────────────────┬───────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
  ┌──────────┐    ┌──────────────┐  ┌──────────┐
  │ Financial │   │ AI Ecosystem │  │Creative  │
  │ Analysis │   │ Monitoring   │  │& Media   │
  └──────────┘    └──────────────┘  └──────────┘
```

See [docs/architecture.md](docs/architecture.md) for the full technical architecture.

## Platform Integrations

| Platform | What's Connected |
|----------|-----------------|
| **Discord** | Primary home channel,Ideas channel for AI briefs, StockMan output |
| **Telegram** | Home delivery channel (disabled for Sachin — banned in India) |
| **Photon** | iMessage integration for mobile |
| **GitHub** | PR workflow, code review, repo management |
| **Kite (Zerodha)** | Real-time prices, order management, portfolio |
| **Google Workspace** | Gmail, Calendar, Drive, Docs |
| **Notion** | Knowledge base and notes |
| **Airtable** | Structured data operations |
| **Philips Hue** | Smart lighting |
| **Ultrahuman Ring** | Health data via Apple Health |

## Configuration Templates

Sample configurations are in `config/templates/`:

```bash
cp config/templates/config.example.yaml config/config.yaml
# Edit with your API keys and preferences
```

## Skills Structure

Each skill is a self-contained package:

```
skills/
└── category/
    └── skill-name/
        ├── SKILL.md           # Main skill definition
        ├── references/        # Supporting docs
        ├── templates/         # Config templates
        └── scripts/          # Helper scripts
```

## Setup

1. Install Hermes Agent
2. Copy `config/templates/config.example.yaml` to `config.yaml`
3. Add your API keys
4. Load skills as needed

See [docs/setup.md](docs/setup.md) for the full setup guide.

## What I Learned

Building this system taught me:
- Multi-agent orchestration with explicit stage gates
- Tool calling and API integration at scale
- Reliable scheduled task execution with multi-platform delivery
- Platform-specific bot development nuances
- Security best practices (env vars, no secrets in files)
- System architecture for composable, maintainable agent systems

## License

MIT License — feel free to use as inspiration for your own projects.

---

*Built with Hermes Agent by Nous Research*
