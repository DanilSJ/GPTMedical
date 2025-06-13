from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="✅ Купить подписку")],
        [KeyboardButton(text="🔻 Описать симптомы")],
        [KeyboardButton(text="🔍 Расшифруй анализы")],
        [KeyboardButton(text="🙋‍♀️ Задать вопрос ИИ-врачу")],
        [KeyboardButton(text="💊 Узнать про лекарство")],
        [KeyboardButton(text="🩸 Женская консультация")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_subscription_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Базовый доступ на неделю — 199₽", callback_data="sub_basic_week")],
        [InlineKeyboardButton(text="Базовый доступ на месяц — 399₽", callback_data="sub_basic_month")],
        [InlineKeyboardButton(text="Расшифровка анализов на неделю — 199₽", callback_data="sub_analysis_week")],
        [InlineKeyboardButton(text="VIP доступ — 699₽", callback_data="sub_vip")],
        [InlineKeyboardButton(text="Premium доступ — 999₽", callback_data="sub_premium")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 