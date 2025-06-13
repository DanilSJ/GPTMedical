from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from src.keyboards.keyboards import get_subscription_keyboard
from src.utils.db_utils import get_or_create_user
from src.services.payment_service import create_payment
from src.database.session import get_session
from config.constants import SubscriptionType
from datetime import datetime, timedelta
from src.models.subscription import Subscription
from config.config import get_settings

settings = get_settings()
router = Router()

@router.message(lambda message: message.text == "✅ Купить подписку")
async def show_subscriptions(message: types.Message):
    await message.answer("Выберите тип подписки:", reply_markup=get_subscription_keyboard())

@router.callback_query(lambda c: c.data.startswith('sub_'))
async def process_subscription(callback_query: types.CallbackQuery):
    subscription_type = callback_query.data.replace('sub_', '')
    subscription_type = SubscriptionType(subscription_type)
    
    async with get_session() as session:
        user = await get_or_create_user(
            session,
            callback_query.from_user.id,
            callback_query.from_user.username,
            callback_query.from_user.first_name,
            callback_query.from_user.last_name
        )
        
        if settings.ENABLE_PAYMENTS:
            # Если платежи включены, создаем платеж
            payment_info = await create_payment(subscription_type, user.id)
            await callback_query.message.answer(
                f"Для оплаты подписки перейдите по ссылке: {payment_info['confirmation_url']}"
            )
        else:
            # Если платежи выключены, активируем подписку автоматически
            end_date = datetime.utcnow() + timedelta(days=30)  # 30 дней подписки
            subscription = Subscription(
                user_id=user.id,
                subscription_type=subscription_type,
                start_date=datetime.utcnow(),
                end_date=end_date,
                is_active=True
            )
            session.add(subscription)
            await session.commit()
            
            await callback_query.message.answer(
                f"✅ Подписка успешно активирована до {end_date.strftime('%d.%m.%Y')}"
            ) 