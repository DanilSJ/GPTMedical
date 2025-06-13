#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.bot.bot import main
from src.database.session import init_db
from src.utils.logger import setup_logger, log_info, log_error

async def startup():
    """Initialize all necessary components before starting the bot"""
    try:
        # Initialize logger
        setup_logger()
        log_info("Logger initialized")
        
        # Initialize database
        log_info("Initializing database...")
        await init_db()
        log_info("Database initialized successfully")
        
        # Start the bot
        log_info("Starting bot...")
        await main()
    except Exception as e:
        log_error(f"Error during startup: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(startup())
    except KeyboardInterrupt:
        log_info("Bot stopped by user")
    except Exception as e:
        log_error(f"Bot stopped due to error: {e}")
        sys.exit(1) 