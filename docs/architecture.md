# Hermes Agent Architecture

High-level system architecture for the Hermes Agent personal assistant system.

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Hermes Agent Core                       │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Skills  │  │  Memory  │  │  Cron    │  │   MCP    │  │
│  │ System  │  │  Layer   │  │Scheduler │  │  Tools   │  │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  │
│       │            │            │            │           │
│  ┌────┴────────────┴────────────┴────────────┴────┐   │
│  │              Tool Orchestration                 │   │
│  └────────────────────┬───────────────────────────┘   │
├──────────────────────┼──────────────────────────────────┤
│           ┌──────────┴──────────┐                      │
│           │   LLM Provider    │                      │
│           │ (Anthropic/OpenAI)│                      │
│           └─────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────┐        ┌─────────┐        ┌─────────┐
   │Discord │        │Telegram │        │  Web   │
   │  Bot   │        │  Bot    │        │Browser │
   └─────────┘        └─────────┘        └─────────┘
```

## Core Components

### 1. Hermes Agent Core
- **Purpose**: Main agent orchestrator
- **Responsibilities**: 
  - LLM interaction
  - Tool call management
  - Conversation state
  - Error handling

### 2. Skills System
- **Purpose**: Modular capability packages
- **Structure**: 
  - SKILL.md (definition)
  - references/ (docs)
  - templates/ (configs)
  - scripts/ (helpers)
- **Loading**: On-demand or startup

### 3. Memory Layer
- **Short-term**: Session memory (injected every turn)
- **Long-term**: OpenViking (semantic search)
- **User Profile**: Persistent preferences

### 4. Cron Scheduler
- **Purpose**: Scheduled task execution
- **Features**:
  - Recurring jobs
  - One-shot jobs
  - Multi-platform delivery
  - Script-based (watchdog)

### 5. MCP Tools
- **Purpose**: External service integration
- **Examples**:
  - Kite (trading)
  - GitHub (PRs, issues)
  - Notion (databases)

## Platform Integrations

### Discord Bot
- Voice effects and ambient sounds
- Thread management
- History backfill
- Rich messages

### Telegram Bot
- Rich messages
- Inline keyboards
- File handling

### WhatsApp
- Business API
- Template messages

## Data Flow

```
User Message
    │
    ▼
Platform Adapter (Discord/Telegram/...)
    │
    ▼
Hermes Agent Core
    │
    ├─▶ Skill Selection
    ├─▶ Memory Injection
    ├─▶ LLM Processing
    └─▶ Tool Execution
    │
    ▼
Response
    │
    ▼
Platform Adapter
    │
    ▼
User
```

## Security Architecture

```
┌─────────────────────────────────┐
│       Environment Variables       │
│   (API keys, tokens, secrets)    │
└─────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│     Config Loading Layer          │
│   (reads .yaml, applies vars)    │
└─────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│    Hermes Agent Runtime         │
│   (tools, skills, cron)        │
└─────────────────────────────────┘
```

### Best Practices
- Never commit secrets
- Use `.gitignore` for config files
- Environment variable substitution
- Secrets in memory, not files
- Regular key rotation

## Scalability Considerations

### Current Setup (Single User)
- Runs on Linux VPS
- ~79 skills loaded
- Multi-platform

### Potential Scale
- Multi-user via Discord/Telegram
- Per-user config
- Rate limiting
- Resource isolation

## Technology Stack

| Component | Technology |
|-----------|-------------|
| Agent Core | Hermes Agent |
| LLM | Anthropic, OpenAI, MiniMax |
| Memory | OpenViking |
| Scheduling | Cron |
| Platforms | Discord, Telegram, WhatsApp |
| Hosting | Linux VPS |

---

*Architecture as of June 2026*