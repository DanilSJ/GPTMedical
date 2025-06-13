from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey, Enum
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
    payment_id: Mapped[Optional[str]] = mapped_column(String(255)) 