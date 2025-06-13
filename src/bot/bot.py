import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.config import get_settings
from src.database.session import init_db
from src.handlers import base, subscription, consultation

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
settings = get_settings()
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

# Register routers
dp.include_router(base.router)
dp.include_router(subscription.router)
dp.include_router(consultation.router)

async def main():
    # Initialize database
    await init_db()
    
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 