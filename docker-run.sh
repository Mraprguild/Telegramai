#!/bin/bash

# Docker run script for Telegram Bot
# This script helps you run the bot with Docker

echo "🤖 Telegram ChatGPT Bot - Docker Setup"
echo "======================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.docker .env
    echo "⚠️  Please edit .env file with your actual API keys before running!"
    echo "   - TELEGRAM_BOT_TOKEN (from @BotFather)"
    echo "   - OPENROUTER_API_KEY (from https://openrouter.ai/keys)"
    echo ""
    read -p "Press Enter after updating .env file..."
fi

# Build and run with Docker Compose
echo "🐳 Building and starting Docker containers..."
docker-compose up --build -d

echo ""
echo "🎉 Bot is starting up!"
echo "📊 Dashboard: http://localhost:5000"
echo "🤖 Bot: Running in background"
echo ""
echo "Useful commands:"
echo "  docker-compose logs -f telegram-bot    # View bot logs"
echo "  docker-compose logs -f web-dashboard   # View dashboard logs"
echo "  docker-compose down                    # Stop all services"
echo "  docker-compose restart                 # Restart services"
echo ""
echo "✅ Setup complete! Check the dashboard at http://localhost:5000"