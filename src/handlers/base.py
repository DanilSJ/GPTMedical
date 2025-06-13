from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from src.keyboards.keyboards import get_main_keyboard
from src.utils.db_utils import get_or_create_user
from src.database.session import get_session
from config.constants import WELCOME_MESSAGE

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    async with get_session() as session:
        user = await get_or_create_user(
            session,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        )
    
    await message.answer(WELCOME_MESSAGE, reply_markup=get_main_keyboard()) 