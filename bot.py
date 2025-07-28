#!/usr/bin/env python3
"""
Telegram ChatGPT Bot

A Telegram bot that integrates with OpenRouter API to provide AI assistant functionality.
The bot responds to user messages using GPT-4o model via OpenRouter.
"""

import logging
import os
from typing import Dict, List
import asyncio
from datetime import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get configuration from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable is required")

# Initialize OpenRouter client (uses OpenAI-compatible API)
openai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# Store conversation history for each user
user_conversations: Dict[int, List[Dict[str, str]]] = {}

class ChatGPTBot:
    """Main bot class handling Telegram bot functionality and ChatGPT integration"""
    
    def __init__(self):
        self.max_conversation_length = 20  # Limit conversation history
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /start command"""
        user = update.effective_user
        welcome_message = (
            f"Hello {user.first_name}! 👋\n\n"
            "I'm an AI assistant powered by ChatGPT. I can help you with:\n"
            "• Answering questions\n"
            "• Creative writing\n"
            "• Problem solving\n"
            "• General conversation\n\n"
            "Just send me a message and I'll respond with AI-generated answers!\n\n"
            "Use /help to see available commands."
        )
        
        await update.message.reply_text(welcome_message)
        logger.info(f"User {user.id} ({user.username}) started the bot")
        
        # Initialize conversation history for new user
        if user.id not in user_conversations:
            user_conversations[user.id] = []

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /help command"""
        help_text = (
            "🤖 *ChatGPT Telegram Bot Help*\n\n"
            "*Available Commands:*\n"
            "/start - Start the bot and get welcome message\n"
            "/help - Show this help message\n"
            "/clear - Clear conversation history\n"
            "/status - Show bot status\n\n"
            "*How to use:*\n"
            "Simply send me any message and I'll respond using ChatGPT!\n\n"
            "*Features:*\n"
            "• Maintains conversation context\n"
            "• Supports long messages\n"
            "• Error handling and retry logic\n"
            "• Real-time responses\n\n"
            "*Note:* The bot remembers your last 20 messages for context."
        )
        
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /clear command to clear conversation history"""
        user_id = update.effective_user.id
        
        if user_id in user_conversations:
            user_conversations[user_id] = []
            await update.message.reply_text("✅ Conversation history cleared!")
        else:
            await update.message.reply_text("📝 No conversation history to clear.")
        
        logger.info(f"User {user_id} cleared conversation history")

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /status command to show bot status"""
        user_id = update.effective_user.id
        conversation_length = len(user_conversations.get(user_id, []))
        
        status_text = (
            "🤖 *Bot Status*\n\n"
            f"✅ Bot is online and operational\n"
            f"💬 Messages in conversation: {conversation_length}\n"
            f"🧠 Model: GPT-4o via OpenRouter\n"
            f"⏰ Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        
        await update.message.reply_text(status_text, parse_mode='Markdown')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle regular text messages and generate ChatGPT responses"""
        user = update.effective_user
        user_message = update.message.text
        user_id = user.id
        
        # Initialize conversation history if not exists
        if user_id not in user_conversations:
            user_conversations[user_id] = []
        
        logger.info(f"Received message from user {user_id} ({user.username}): {user_message[:50]}...")
        
        # Send typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            # Add user message to conversation history
            user_conversations[user_id].append({
                "role": "user", 
                "content": user_message
            })
            
            # Limit conversation history length
            if len(user_conversations[user_id]) > self.max_conversation_length:
                user_conversations[user_id] = user_conversations[user_id][-self.max_conversation_length:]
            
            # Generate response using ChatGPT
            response = await self.generate_chatgpt_response(user_id)
            
            # Add assistant response to conversation history
            user_conversations[user_id].append({
                "role": "assistant", 
                "content": response
            })
            
            # Send response to user
            await self.send_long_message(update, response)
            
            logger.info(f"Sent response to user {user_id}: {response[:50]}...")
            
        except Exception as e:
            error_message = (
                "❌ I'm sorry, I encountered an error while processing your message. "
                "Please try again in a moment.\n\n"
                f"Error details: {str(e)}"
            )
            await update.message.reply_text(error_message)
            logger.error(f"Error handling message for user {user_id}: {e}")

    async def generate_chatgpt_response(self, user_id: int) -> str:
        """Generate response using OpenAI ChatGPT API"""
        try:
            # Prepare messages for API call
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI assistant integrated into a Telegram bot. "
                        "Provide clear, concise, and helpful responses. "
                        "You can use emojis when appropriate to make conversations more engaging. "
                        "Keep responses conversational and friendly."
                    )
                }
            ]
            
            # Add conversation history
            messages.extend(user_conversations[user_id])
            
            # Make API call to OpenRouter using GPT-4o via OpenRouter
            response = openai_client.chat.completions.create(
                model="openai/gpt-4o",  # OpenRouter format for GPT-4o
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating ChatGPT response: {e}")
            raise Exception(f"Failed to generate AI response: {str(e)}")

    async def send_long_message(self, update: Update, message: str, max_length: int = 4096) -> None:
        """Send long messages by splitting them if they exceed Telegram's limit"""
        if len(message) <= max_length:
            await update.message.reply_text(message)
        else:
            # Split message into chunks
            for i in range(0, len(message), max_length):
                chunk = message[i:i + max_length]
                await update.message.reply_text(chunk)
                # Small delay between chunks to avoid rate limiting
                await asyncio.sleep(0.1)

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Global error handler for the bot"""
        logger.error(f"Exception while handling an update: {context.error}")
        
        # Try to send error message to user if update contains a message
        if isinstance(update, Update) and update.message:
            try:
                await update.message.reply_text(
                    "❌ An unexpected error occurred. Please try again later."
                )
            except Exception:
                pass  # Ignore if we can't send error message

async def main() -> None:
    """Main function to run the bot"""
    logger.info("Starting ChatGPT Telegram Bot...")
    
    # Create bot instance
    bot = ChatGPTBot()
    
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("clear", bot.clear_command))
    application.add_handler(CommandHandler("status", bot.status_command))
    
    # Add message handler for regular text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    # Add error handler
    application.add_error_handler(bot.error_handler)
    
    # Initialize the application
    await application.initialize()
    
    # Start the bot
    logger.info("Bot is starting... Press Ctrl+C to stop.")
    
    try:
        # Run the bot until the user presses Ctrl-C
        await application.start()
        await application.updater.start_polling()
        
        # Keep the bot running
        import signal
        stop_signals = (signal.SIGTERM, signal.SIGINT)
        for s in stop_signals:
            signal.signal(s, lambda s, f: asyncio.create_task(application.stop()))
        
        # Wait until the application is stopped
        while application.updater.running:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error running bot: {e}")
    finally:
        await application.stop()
        await application.shutdown()
        logger.info("ChatGPT Telegram Bot stopped.")

if __name__ == '__main__':
    asyncio.run(main())
