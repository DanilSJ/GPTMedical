from yookassa import Configuration, Payment
from datetime import datetime, timedelta
from config.config import get_settings
from config.constants import SubscriptionType, SUBSCRIPTION_PRICES, SUBSCRIPTION_DURATIONS

settings = get_settings()

# Configure YooKassa
Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

async def create_payment(subscription_type: SubscriptionType, user_id: int) -> dict:
    """
    Create a new payment in YooKassa
    """
    payment = Payment.create({
        "amount": {
            "value": str(SUBSCRIPTION_PRICES[subscription_type]),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"https://t.me/dwdwedfwfewafewa_bot"  # Replace with your bot username
        },
        "capture": True,
        "description": f"Подписка {subscription_type.value}",
        "metadata": {
            "user_id": user_id,
            "subscription_type": subscription_type.value
        }
    })
    
    return {
        "payment_id": payment.id,
        "confirmation_url": payment.confirmation.confirmation_url
    }

async def check_payment(payment_id: str) -> bool:
    """
    Check payment status in YooKassa
    """
    payment = Payment.find_one(payment_id)
    return payment.status == "succeeded"

def get_subscription_end_date(subscription_type: SubscriptionType) -> datetime:
    """
    Calculate subscription end date based on type
    """
    return datetime.utcnow() + timedelta(days=SUBSCRIPTION_DURATIONS[subscription_type]) 