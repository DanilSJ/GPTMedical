import openai
import logging
from typing import Optional
from config.config import get_settings
from config.constants import GPT_SYSTEM_PROMPT

settings = get_settings()
client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

logger = logging.getLogger(__name__)

async def get_gpt_response(
    message: str,
    context: Optional[str] = None,
    is_female_consultation: bool = False
) -> str:
    """
    Get response from GPT-4
    """
    messages = [
        {"role": "system", "content": GPT_SYSTEM_PROMPT}
    ]
    
    if is_female_consultation:
        messages.append({
            "role": "system",
            "content": "Отвечай как опытный гинеколог, сохраняя профессиональный, но дружелюбный тон."
        })
    
    if context:
        messages.append({"role": "system", "content": context})
    
    messages.append({"role": "user", "content": message})
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in GPT response: {str(e)}", exc_info=True)
        return f"Извините, произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте позже."

async def analyze_medical_document(document_text: str) -> str:
    """
    Analyze medical document (test results, etc.)
    """
    prompt = f"""Проанализируй следующие медицинские данные и предоставь понятное объяснение:
    
    {document_text}
    
    Пожалуйста, объясни результаты простым языком и укажи, если есть какие-то отклонения от нормы."""
    
    return await get_gpt_response(prompt, context="Ты - опытный врач-лаборант, который анализирует медицинские документы и результаты анализов.") 