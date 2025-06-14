from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.subscription import Subscription
from src.utils.db_utils import check_user_subscription
from config.constants import SUBSCRIPTION_PRICES
from src.utils.logger import log_error, log_info
from sqlalchemy import select

class SubscriptionService:
    """Сервис для работы с подписками"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def check_subscription(self, user_id: int) -> bool:
        """Проверка наличия активной подписки"""
        return await check_user_subscription(self.session, user_id)
    
    async def create_subscription(
        self, 
        user_id: int, 
        subscription_type: str, 
        duration_days: int,
        payment_id: str = None,
        payment_status: str = None,
        payment_method: str = None,
        payment_description: str = None
    ) -> bool:
        """Создание новой подписки"""
        try:
            now = datetime.utcnow()
            log_info(f"Creating subscription for user {user_id}, type: {subscription_type}")
            
            # Проверяем, нет ли уже активной подписки
            existing_subscription = await self.session.execute(
                select(Subscription).where(
                    Subscription.user_id == user_id,
                    Subscription.is_active == True,
                    Subscription.end_date > now
                )
            )
            if existing_subscription.first():
                log_info(f"User {user_id} already has an active subscription")
                return True

            subscription = Subscription(
                user_id=user_id,
                subscription_type=subscription_type,
                start_date=now,
                end_date=now + timedelta(days=duration_days),
                is_active=True,
                payment_id=payment_id,
                payment_amount=SUBSCRIPTION_PRICES[subscription_type],
                payment_status=payment_status,
                payment_created_at=now,
                payment_paid_at=now if payment_status == "succeeded" else None,
                payment_method=payment_method,
                payment_description=payment_description
            )
            self.session.add(subscription)
            await self.session.commit()
            log_info(f"Successfully created subscription for user {user_id}")
            return True
        except Exception as e:
            await self.session.rollback()
            log_error(f"Error creating subscription for user {user_id}: {str(e)}")
            return False 