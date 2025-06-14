from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey, Enum, Float
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from config.constants import SubscriptionType

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subscription_type: Mapped[SubscriptionType]
    start_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    end_date: Mapped[datetime]
    is_active: Mapped[bool] = mapped_column(default=True)
    
    # Поля для отслеживания платежей
    payment_id: Mapped[Optional[str]] = mapped_column(String(255))
    payment_amount: Mapped[Optional[float]] = mapped_column(Float)
    payment_status: Mapped[Optional[str]] = mapped_column(String(50))
    payment_created_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    payment_paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    payment_method: Mapped[Optional[str]] = mapped_column(String(50))
    payment_description: Mapped[Optional[str]] = mapped_column(String(255)) 