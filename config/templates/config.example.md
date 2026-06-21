# Hermes Agent Configuration Template

This is a template configuration. Copy to `config.yaml` and customize with your values.

## Usage

```bash
cp config/templates/config.example.yaml ../config.yaml
# Edit the file with your API keys and preferences
```

## Model Configuration

```yaml
model:
  default: anthropic-sonnet-4
  provider: anthropic
  # Get from your provider dashboard
  api_key: YOUR_ANTHROPIC_API_KEY
```

## Tool Sets

```yaml
toolsets:
  - terminal      # Shell commands
  - file          # File operations
  - web           # Web search
  - browser       # Browser automation
  - code_exec     # Python execution
```

## Platform Integration

```yaml
telegram:
  bot_token: YOUR_TELEGRAM_BOT_TOKEN
  allowed_chats:
    - YOUR_CHAT_ID

discord:
  bot_token: YOUR_DISCORD_BOT_TOKEN
  server_id: YOUR_SERVER_ID
  channel_prompts: {}
```

## Additional Providers

```yaml
openrouter:
  api_key: YOUR_OPENROUTER_API_KEY

huggingface:
  api_key: YOUR_HF_API_KEY

serper:
  api_key: YOUR_SERPER_API_KEY
```

## Memory

```yaml
memory:
  provider: openviking
  # Configure if using OpenViking
  api_key: YOUR_VIKING_API_KEY
```

## Cron Jobs

```yaml
# Add scheduled tasks
cron:
  enabled: true
  jobs:
    - name: daily-briefing
      schedule: "0 9 * * *"
      prompt: "Summarize today's news"
```

## Security Notes

- Never commit this file to version control
- Add `config.yaml` to your `.gitignore`
- Use environment variables for sensitive values in production
- Rotate API keys regularly

## Full Configuration Options

See the [Hermes Agent Documentation](https://hermes-agent.nousresearch.com/docs) for all available options.