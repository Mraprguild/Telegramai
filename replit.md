# Telegram ChatGPT Bot

## Overview

This is a Telegram bot that integrates with OpenAI's ChatGPT API to provide AI assistant functionality. The bot responds to user messages using the GPT-4o model and maintains conversation history for each user.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a simple monolithic architecture with the following components:

- **Bot Framework**: Python-based Telegram bot using the `python-telegram-bot` library
- **AI Integration**: Direct integration with OpenAI's API for chat completions
- **Data Storage**: In-memory storage for conversation history (no persistent database)
- **Configuration**: Environment variable-based configuration using dotenv

## Key Components

### Bot Handler (`bot.py`)
- **Purpose**: Main application file containing the Telegram bot logic
- **Responsibilities**: 
  - Handles incoming Telegram messages
  - Manages conversation state in memory
  - Integrates with OpenRouter API for response generation
  - Implements conversation history management with a 20-message limit

### ChatGPTBot Class
- **Architecture Decision**: Object-oriented approach for bot functionality
- **Rationale**: Encapsulates bot behavior and makes the code more maintainable
- **Key Features**: 
  - Conversation length limiting to manage API costs and context size
  - User-specific conversation tracking

## Data Flow

1. User sends message to Telegram bot
2. Bot receives update via Telegram Bot API
3. Message is processed and added to user's conversation history
4. Complete conversation context is sent to OpenRouter API
5. GPT response is received and sent back to user via Telegram
6. Response is added to conversation history

## External Dependencies

### Required APIs
- **Telegram Bot API**: For receiving and sending messages
- **OpenRouter API**: For GPT-4o chat completions (switched from direct OpenAI for better reliability and pricing)

### Python Libraries
- `python-telegram-bot`: Telegram bot framework
- `openai`: OpenAI-compatible Python client (used for OpenRouter API)
- `python-dotenv`: Environment variable management

### Environment Variables
- `TELEGRAM_BOT_TOKEN`: Required for Telegram Bot API authentication
- `OPENROUTER_API_KEY`: Required for OpenRouter API access

## Deployment Strategy

### Current Setup
- **Environment**: Designed for Replit deployment
- **Process Management**: Single Python process
- **State Management**: In-memory only (conversation history lost on restart)

### Architectural Considerations
- **Scalability**: Current in-memory storage limits scalability to single instance
- **Persistence**: No database integration means conversation history is not preserved across restarts
- **Future Enhancement**: Could benefit from adding persistent storage (e.g., PostgreSQL with Drizzle ORM) for conversation history and user preferences

### Deployment Requirements
- Python 3.7+ runtime
- Environment variables properly configured
- Continuous process execution (bot needs to stay running to receive updates)

## Key Design Decisions

### In-Memory Storage
- **Problem**: Need to track conversation history per user
- **Solution**: Python dictionary storing user conversations in memory
- **Pros**: Simple implementation, fast access
- **Cons**: Data lost on restart, memory usage grows over time, not scalable across multiple instances

### Conversation Length Limiting
- **Problem**: OpenAI API has token limits and costs scale with conversation length
- **Solution**: Limit conversation history to 20 messages per user
- **Rationale**: Balances context preservation with cost and API constraints

### Direct API Integration
- **Problem**: Need to integrate with both Telegram and OpenAI
- **Solution**: Direct API calls using official libraries
- **Pros**: Simple, reliable, well-documented
- **Cons**: No abstraction layer for potential future AI provider changes