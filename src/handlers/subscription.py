from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from src.keyboards.keyboards import get_subscription_keyboard
from src.utils.db_utils import get_or_create_user
from src.services.payment_service import create_payment, check_payment, get_subscription_end_date
from src.database.session import get_session
from config.constants import SubscriptionType, SUBSCRIPTION_DURATIONS
from datetime import datetime, timedelta
from src.models.subscription import Subscription
from config.config import get_settings
from src.services.subscription_service import SubscriptionService
from yookassa import Payment
from sqlalchemy import select
from src.utils.logger import log_error

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
            
            # Создаем клавиатуру с кнопкой проверки платежа
            keyboard = types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [types.InlineKeyboardButton(
                        text="✅ Проверить оплату",
                        callback_data=f"verify_payment_{payment_info['payment_id']}"
                    )]
                ]
            )
            
            await callback_query.message.answer(
                f"Для оплаты подписки перейдите по ссылке: {payment_info['confirmation_url']}\n\n"
                "После оплаты нажмите кнопку 'Проверить оплату'",
                reply_markup=keyboard
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

@router.callback_query(lambda c: c.data.startswith('verify_payment_'))
async def verify_payment(callback_query: types.CallbackQuery):
    payment_id = callback_query.data.replace('verify_payment_', '')
    
    async with get_session() as session:
        try:
            # Проверяем статус платежа
            payment_success = await check_payment(payment_id)
            
            if payment_success:
                # Получаем информацию о платеже
                payment = Payment.find_one(payment_id)
                user_id = payment.metadata.get('user_id')
                subscription_type = SubscriptionType(payment.metadata.get('subscription_type'))
                
                # Проверяем, не был ли уже создан платеж
                existing_subscription = await session.execute(
                    select(Subscription).where(Subscription.payment_id == payment_id)
                )
                if existing_subscription.first():
                    await callback_query.message.answer(
                        "✅ Подписка уже была активирована ранее. "
                        "Вы можете продолжать пользоваться ботом."
                    )
                    return
                
                # Создаем подписку
                subscription_service = SubscriptionService(session)
                success = await subscription_service.create_subscription(
                    user_id=user_id,
                    subscription_type=subscription_type.value,
                    duration_days=SUBSCRIPTION_DURATIONS[subscription_type],
                    payment_id=payment.id,
                    payment_status=payment.status,
                    payment_method=payment.payment_method.type if payment.payment_method else None,
                    payment_description=payment.description
                )
                
                if success:
                    end_date = get_subscription_end_date(subscription_type)
                    await callback_query.message.answer(
                        f"✅ Оплата прошла успешно!\n"
                        f"Ваша подписка активирована до {end_date.strftime('%d.%m.%Y')}\n"
                        f"Теперь вам доступны все функции бота!"
                    )
                else:
                    await callback_query.message.answer(
                        "❌ Произошла ошибка при активации подписки.\n"
                        "Пожалуйста, напишите в поддержку и укажите:\n"
                        f"- ID платежа: {payment_id}\n"
                        f"- Тип подписки: {subscription_type.value}"
                    )
            else:
                await callback_query.message.answer(
                    "❌ Платеж не найден или не был завершен.\n"
                    "Пожалуйста, попробуйте оплатить снова или обратитесь в поддержку."
                )
        except Exception as e:
            log_error(f"Error in payment verification: {str(e)}")
            await callback_query.message.answer(
                "❌ Произошла ошибка при проверке платежа.\n"
                "Пожалуйста, напишите в поддержку и укажите:\n"
                f"- ID платежа: {payment_id}"
            ) 