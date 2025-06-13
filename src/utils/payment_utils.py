import requests
from config.config import get_settings

settings = get_settings()

def create_payment(amount: int, description: str) -> str:
    """Создание платежа"""
    try:
        response = requests.post(
            f"{settings.PAYMENT_API_URL}/payments",
            json={
                "amount": amount,
                "description": description
            },
            headers={"Authorization": f"Bearer {settings.PAYMENT_API_KEY}"}
        )
        response.raise_for_status()
        return response.json()["id"]
    except Exception as e:
        print(f"Error creating payment: {str(e)}")
        return None

def verify_payment(payment_id: str) -> bool:
    """Проверка статуса платежа"""
    try:
        response = requests.get(
            f"{settings.PAYMENT_API_URL}/payments/{payment_id}",
            headers={"Authorization": f"Bearer {settings.PAYMENT_API_KEY}"}
        )
        response.raise_for_status()
        return response.json()["status"] == "succeeded"
    except Exception as e:
        print(f"Error verifying payment: {str(e)}")
        return False 