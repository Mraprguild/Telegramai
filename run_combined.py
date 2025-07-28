#!/usr/bin/env python3
"""
Combined Bot and Web Server Runner

Runs both the Telegram bot and web dashboard in the same process.
"""

import os
import asyncio
import threading
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_web_server():
    """Run the Flask web server in a separate thread"""
    try:
        from web_server import run_server
        logger.info("Starting web server thread...")
        run_server()
    except Exception as e:
        logger.error(f"Web server error: {e}")

async def run_telegram_bot():
    """Run the Telegram bot"""
    try:
        # Import and run the bot
        from bot import main as bot_main
        logger.info("Starting Telegram bot...")
        await bot_main()
    except Exception as e:
        logger.error(f"Telegram bot error: {e}")

def main():
    """Main function to run both services"""
    logger.info("Starting combined Telegram Bot and Web Dashboard...")
    
    # Start web server in a separate thread
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # Wait a moment for web server to start
    import time
    time.sleep(2)
    
    # Run the Telegram bot in the main thread
    try:
        asyncio.run(run_telegram_bot())
    except KeyboardInterrupt:
        logger.info("Shutting down services...")
    except Exception as e:
        logger.error(f"Error running combined services: {e}")
    finally:
        logger.info("Combined services stopped.")

if __name__ == '__main__':
    main()