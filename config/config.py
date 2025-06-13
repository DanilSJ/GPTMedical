from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # Bot settings
    BOT_TOKEN: str
    
    # Database settings
    DATABASE_URL: str = "sqlite+aiosqlite:///doctor_gpt.db"
    
    # Payment settings
    ENABLE_PAYMENTS: bool = True  # Включена ли платежная система
    YOOKASSA_SHOP_ID: str
    YOOKASSA_SECRET_KEY: str
    
    # OpenAI settings
    OPENAI_API_KEY: str
    
    # Subscription settings
    FREE_MESSAGE_LIMIT: int = 10
    DAILY_MESSAGE_LIMIT: int = 1000
    
    # Logging settings
    ENABLE_LOGS: bool = True  # Включены ли логи
    LOG_LEVEL: str = "INFO"  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings() 