import logging
import os
from pathlib import Path
from config.config import get_settings

settings = get_settings()

def setup_logger():
    """
    Настраивает логгер с учетом настроек из конфига
    """
    if not settings.ENABLE_LOGS:
        logging.getLogger().setLevel(logging.CRITICAL)  # Отключаем все логи
        return

    # Создаем директорию для логов если её нет
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Путь к файлу лога
    log_file = log_dir / "bot.log"
    
    # Настраиваем формат логов
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)
    
    # Настраиваем файловый обработчик
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # Настраиваем консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Получаем корневой логгер
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Очищаем существующие обработчики
    logger.handlers.clear()
    
    # Добавляем обработчики
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Логируем начало работы
    logger.info("Logger initialized")

def log_debug(message: str):
    """Логирование отладочной информации"""
    if settings.ENABLE_LOGS:
        logging.debug(message)

def log_info(message: str):
    """Логирование информационных сообщений"""
    if settings.ENABLE_LOGS:
        logging.info(message)

def log_warning(message: str):
    """Логирование предупреждений"""
    if settings.ENABLE_LOGS:
        logging.warning(message)

def log_error(message: str):
    """Логирование ошибок"""
    if settings.ENABLE_LOGS:
        logging.error(message)

def log_critical(message: str):
    """Логирование критических ошибок"""
    if settings.ENABLE_LOGS:
        logging.critical(message) 