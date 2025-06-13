from aiogram import Router, types
from config.constants import WELCOME_MESSAGE

router = Router()

@router.message()
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    if message.text == "/start":
        await message.answer(WELCOME_MESSAGE) 