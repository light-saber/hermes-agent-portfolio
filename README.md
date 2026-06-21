# Hermes Agent Portfolio

A personal AI assistant agent system built with Hermes Agent, showcasing capabilities in automation, multi-platform integration, financial analysis, creative content generation, and more.

## What This Is

This repository demonstrates skills in building and managing AI agents for personal productivity and automation use cases. It includes:

- **79+ specialized skills** across 15 categories
- **Multi-platform integration** (Discord, Telegram, WhatsApp)
- **Financial analysis** with stock trading automation
- **Creative workflows** for content generation
- **ML/MLOps pipelines** for model deployment
- **Multi-agent orchestration** for complex workflows

## Core Capabilities

### Multi-Platform Integration
- Discord bot with voice effects and ambient sounds
- Telegram bot with rich messages
- WhatsApp business integration
- Scheduled task delivery to multiple platforms

### Financial Analysis
- Stock screening and research
- Real-time price lookups (NSE/US)
- Portfolio analysis
- Trading order management via Kite API

### Creative & Media
- ASCII art and video generation
- HTML artifacts and infographics
- YouTube content processing
- AI music generation prompts
- Design system implementations

### Productivity
- Email management (IMAP/SMTP)
- Calendar and document automation
- Notion, Airtable, Google Workspace integration
- PDF/document OCR and editing
- Meeting pipeline automation

### MLOps & Development
- Local LLM inference (llama.cpp)
- Model benchmarking (lm-eval-harness)
- HuggingFace model management
- vLLM serving
- Code review and PR workflows

### Automation & DevOps
- Tailscale remote access
- Kanban workflow automation
- Cron-based scheduled tasks
- Multi-agent task routing

## Skills Overview

| Category | Count | Examples |
|----------|-------|----------|
| autonomous-ai-agents | 5 | Claude Code, Codex, OpenCode, staged workflows |
| creative | 15 | ASCII art, HTML artifacts, design systems |
| financial-analysis | 1 | Stock analysis |
| github | 5 | Auth, PR workflow, code review |
| mlops | 7 | llama.cpp, vLLM, HuggingFace |
| productivity | 14 | Email, maps, Notion, PowerPoint |
| research | 8 | arXiv, flight search, Polymarket |
| software-development | 8 | Debugging, TDD, spike workflows |

See [SKILLS.md](SKILLS.md) for detailed skill inventory.

## Architecture

The system consists of:
- **Hermes Agent Core**: LLM-powered agent with tool orchestration
- **Skill System**: Modular skill files with reusable workflows
- **Platform Adapters**: Discord, Telegram, WhatsApp integrations
- **Memory Layer**: Short-term (session) + long-term (OpenViking)
- **Cron Scheduler**: Scheduled task execution
- **MCP Tools**: Model Context Protocol for external integrations

See [docs/architecture.md](docs/architecture.md) for detailed architecture.

## Configuration Templates

Sample configurations are in `config/templates/`. Copy and customize:

```bash
cp config/templates/config.example.yaml config/config.yaml
# Edit with your API keys and preferences
```

## Skills Structure

Skills follow a standard format:

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

See [docs/setup.md](docs/setup.md) for full setup guide.

## What I Learned

Building this system taught me:
- Multi-agent orchestration patterns
- Tool calling and API integration
- Scheduled task management
- Platform-specific bot development
- Security best practices (API key management)
- System architecture design

## License

MIT License - feel free to use as inspiration for your own projects.

---

*Built with Hermes Agent by Nous Research*