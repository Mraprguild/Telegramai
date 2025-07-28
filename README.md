# Telegram ChatGPT Bot

A powerful Telegram bot that integrates with OpenRouter API to provide AI assistant functionality using GPT-4o. Features include conversation memory, web dashboard monitoring, and Docker deployment support.

## Features

- 🤖 **ChatGPT Integration**: Uses GPT-4o model via OpenRouter API for intelligent responses
- 💬 **Conversation Memory**: Maintains context of last 20 messages per user
- 🌐 **Web Dashboard**: Real-time monitoring and status checking
- 🔄 **Webhook Support**: Both polling and webhook modes supported
- 🐳 **Docker Ready**: Complete containerization with Docker Compose
- 📊 **Health Monitoring**: Built-in health checks and status endpoints
- ⚡ **Error Handling**: Robust error handling with graceful fallbacks

## Quick Start

### Option 1: Replit (Recommended)

1. **Get API Keys**:
   - Telegram: Message [@BotFather](https://t.me/botfather) to create a bot
   - OpenRouter: Get API key from [openrouter.ai/keys](https://openrouter.ai/keys)

2. **Configure Secrets**:
   - Add `TELEGRAM_BOT_TOKEN` to Replit Secrets
   - Add `OPENROUTER_API_KEY` to Replit Secrets

3. **Run**: The bot starts automatically!

### Option 2: Docker Deployment

1. **Clone and Setup**:
   ```bash
   git clone <your-repo>
   cd telegram-chatgpt-bot
   ```

2. **Configure Environment**:
   ```bash
   cp .env.docker .env
   # Edit .env with your API keys
   ```

3. **Run with Docker**:
   ```bash
   ./docker-run.sh
   ```

4. **Access Dashboard**: http://localhost:5000

### Option 3: Local Development

1. **Install Dependencies**:
   ```bash
   pip install python-telegram-bot openai python-dotenv flask
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run Bot**:
   ```bash
   python bot.py
   ```

4. **Run Dashboard** (optional):
   ```bash
   python web_server.py
   ```

## Bot Commands

- `/start` - Initialize bot and get welcome message
- `/help` - Show all available commands and features
- `/clear` - Clear conversation history
- `/status` - Show bot status and statistics

## Web Dashboard

The web dashboard provides:

- **Real-time Status**: Bot online/offline status
- **API Monitoring**: OpenRouter API connection status
- **Performance Metrics**: Response times and user activity
- **Webhook Configuration**: Easy webhook URL management
- **Health Checks**: System health monitoring

Access at: `http://localhost:5000` (or your Replit URL)

## Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f telegram-bot
docker-compose logs -f web-dashboard

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build -d

# Scale services
docker-compose up -d --scale telegram-bot=2
```

## API Endpoints

- `GET /` - Web dashboard
- `GET /api/status` - Bot status JSON
- `POST /webhook` - Telegram webhook endpoint
- `GET /health` - Health check endpoint

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | Yes |
| `OPENROUTER_API_KEY` | OpenRouter API key | Yes |
| `PORT` | Web server port (default: 5000) | No |
| `BOT_WEBHOOK_URL` | Webhook URL for production | No |

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Telegram API   │ ←→ │  Python Bot      │ ←→ │ OpenRouter API  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ↓
                       ┌──────────────────┐
                       │  Flask Dashboard │
                       └──────────────────┘
                              │
                              ↓
                       ┌──────────────────┐
                       │   Web Interface  │
                       └──────────────────┘
```

## Development

### File Structure

```
├── bot.py              # Main bot application
├── web_server.py       # Web dashboard server
├── run_combined.py     # Combined bot + web server
├── index.html          # Dashboard frontend
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Multi-service setup
├── .env.docker         # Environment template
└── README.md          # This file
```

### Adding Features

1. **New Bot Commands**: Add handlers in `bot.py`
2. **Dashboard Features**: Modify `web_server.py` and `index.html`
3. **Docker Changes**: Update `Dockerfile` and `docker-compose.yml`

## Troubleshooting

### Common Issues

1. **Bot Not Responding**:
   - Check API keys are correct
   - Verify bot token with @BotFather
   - Check OpenRouter account has credits

2. **Webhook Not Working**:
   - Ensure URL is publicly accessible
   - Check webhook endpoint is responding
   - Verify SSL certificate (HTTPS required)

3. **Docker Issues**:
   - Check `.env` file exists and has correct values
   - Ensure ports 5000-5001 are not in use
   - Run `docker-compose logs` to check errors

### Logs

- **Bot Logs**: Check Replit console or `docker-compose logs telegram-bot`
- **Web Logs**: Check `docker-compose logs web-dashboard`
- **Health Status**: Visit `/health` endpoint

## License

MIT License - Feel free to use and modify!

## Support

For issues:
1. Check logs for error messages
2. Verify API keys and credentials
3. Test with `/status` command
4. Check web dashboard at `/health`

---

Built with ❤️ using Python, OpenRouter, and Docker