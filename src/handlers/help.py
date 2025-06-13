from aiogram import Router, types
from config.constants import HELP_MESSAGE

router = Router()

@router.message()
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    if message.text == "/help":
        await message.answer(HELP_MESSAGE) 