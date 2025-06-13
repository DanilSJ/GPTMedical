import logging
from config.config import get_settings

settings = get_settings()

def setup_logger():
    """
    Настраивает логгер с учетом настроек из конфига
    """
    if not settings.ENABLE_LOGS:
        logging.getLogger().setLevel(logging.CRITICAL)  # Отключаем все логи
        return

    # Настраиваем формат логов
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format=log_format,
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler()
        ]
    )

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