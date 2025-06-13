from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.subscription import Subscription
from src.utils.db_utils import check_user_subscription

class SubscriptionService:
    """Сервис для работы с подписками"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def check_subscription(self, user_id: int) -> bool:
        """Проверка наличия активной подписки"""
        return await check_user_subscription(self.session, user_id)
    
    async def create_subscription(self, user_id: int, subscription_type: str, duration_days: int) -> bool:
        """Создание новой подписки"""
        try:
            subscription = Subscription(
                user_id=user_id,
                subscription_type=subscription_type,
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=duration_days),
                is_active=True
            )
            self.session.add(subscription)
            await self.session.commit()
            return True
        except Exception:
            await self.session.rollback()
            return False 