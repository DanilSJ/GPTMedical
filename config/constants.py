from enum import Enum

class SubscriptionType(str, Enum):
    BASIC_WEEK = "basic_week"
    BASIC_MONTH = "basic_month"
    ANALYSIS_WEEK = "analysis_week"
    VIP = "vip"
    PREMIUM = "premium"

SUBSCRIPTION_PRICES = {
    SubscriptionType.BASIC_WEEK: 199.0,
    SubscriptionType.BASIC_MONTH: 399.0,
    SubscriptionType.ANALYSIS_WEEK: 199.0,
    SubscriptionType.VIP: 699.0,
    SubscriptionType.PREMIUM: 999.0
}

SUBSCRIPTION_DURATIONS = {
    SubscriptionType.BASIC_WEEK: 7,  # days
    SubscriptionType.BASIC_MONTH: 30,
    SubscriptionType.ANALYSIS_WEEK: 7,
    SubscriptionType.VIP: 30,
    SubscriptionType.PREMIUM: 30
}

WELCOME_MESSAGE = """Привет, я Доктор GPT 👨‍⚕️
Расскажи, что болит, или выбери вопрос ниже👇
▫️ Всё, что я говорю — справочно. Если серьёзно — рекомендую обратиться к врачу."""

HELP_MESSAGE = """Я могу помочь вам с:
1. 🔻 Описать симптомы - расскажите о своих симптомах
2. 🔍 Расшифровать анализы - отправьте фото или файл с анализами
3. 🙋‍♀️ Задать вопрос ИИ-врачу - задайте любой медицинский вопрос
4. 💊 Узнать про лекарство - получите информацию о препаратах
5. 🩸 Женская консультация - вопросы по женскому здоровью

Для использования всех функций необходимо приобрести подписку."""

GPT_SYSTEM_PROMPT = """Ты — медицинский помощник, который говорит по-человечески, как опытный врач с сочувствием, но без занудства. 
Отвечай кратко, дружелюбно, как будто общаешься с человеком лично. 
Не пиши длинных сухих текстов, не пересказывай Википедию. 
Если спрашивают что-то серьёзное — уточни 2–3 вопроса, потом дай простой ответ и добавь совет, если надо обратиться к врачу — скажи это мягко и понятно.

Общайся с людьми как ChatGPT в Telegram, живо, без ИИ-шных фраз вроде "я понимаю вашу озабоченность". 
Не используй формальный стиль."""

SUBSCRIPTION_MESSAGE_NOT_ENOUGH_MESSAGES = """Для продолжения общения необходимо приобрести подписку."""