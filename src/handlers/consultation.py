from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from src.core.states import UserState
from src.utils.db_utils import get_or_create_user, check_user_subscription
from src.services.gpt_service import get_gpt_response
from src.database.session import get_session
from config.config import get_settings
from config.constants import SUBSCRIPTION_MESSAGE_NOT_ENOUGH_MESSAGES
from src.services.document_service import DocumentService
from src.utils.logger import log_info, log_error, log_debug

router = Router()
settings = get_settings()

@router.message(lambda message: message.text == "🔻 Описать симптомы")
async def handle_symptoms(message: types.Message, state: FSMContext):
    await state.set_state(UserState.waiting_for_symptoms)
    await message.answer("Пожалуйста, опишите ваши симптомы подробно. Это поможет мне лучше понять вашу ситуацию.")

@router.message(UserState.waiting_for_symptoms)
async def process_symptoms(message: types.Message, state: FSMContext):
    async with get_session() as session:
        user = await get_or_create_user(
            session,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        )
        
        has_subscription = await check_user_subscription(session, user.id)
        
        if not has_subscription and user.message_count >= settings.FREE_MESSAGE_LIMIT:
            await message.answer(SUBSCRIPTION_MESSAGE_NOT_ENOUGH_MESSAGES)
            return
        
        response = await get_gpt_response(message.text)
        await message.answer(response)
        
        if not has_subscription:
            user.message_count += 1
            await session.commit()

@router.message(lambda message: message.text == "🔍 Расшифруй анализы")
async def handle_analysis(message: types.Message, state: FSMContext):
    await state.set_state(UserState.waiting_for_analysis)
    await message.answer("Пожалуйста, отправьте фото или файл с вашими анализами.")

@router.message(UserState.waiting_for_analysis)
async def process_analysis(message: types.Message, state: FSMContext):
    async with get_session() as session:
        user = await get_or_create_user(
            session,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        )
        
        has_subscription = await check_user_subscription(session, user.id)
        
        if not has_subscription and user.message_count >= settings.FREE_MESSAGE_LIMIT:
            await message.answer(SUBSCRIPTION_MESSAGE_NOT_ENOUGH_MESSAGES)
            return

        # Проверяем, есть ли документ
        if message.document:
            await message.answer("Получил ваши анализы. Обрабатываю...")
            
            # Получаем файл
            file = await message.bot.get_file(message.document.file_id)
            log_debug(f"Downloading file: {message.document.file_name}")
            file_data = await message.bot.download_file(file.file_path)
            file_bytes = file_data.read()  # Читаем байты из BytesIO
            log_debug(f"File downloaded, size: {len(file_bytes)} bytes")
            
            # Извлекаем текст из документа
            document_text = await DocumentService.extract_text_from_document(file_bytes, message.document.file_name)
            
            if document_text:
                log_info(f"Successfully extracted text, length: {len(document_text)} characters")
                # Формируем запрос к GPT
                prompt = f"""Проанализируй следующие медицинские анализы и дай краткое заключение:
                
                {document_text}
                
                Пожалуйста, укажи:
                1. Какие показатели в норме
                2. Какие показатели отклонены от нормы
                3. Общее заключение
                4. Рекомендации (если есть отклонения)
                """
                
                response = await get_gpt_response(prompt)
                await message.answer(response)
            else:
                log_error("Failed to extract text from document")
                await message.answer("Извините, не удалось прочитать документ. Пожалуйста, убедитесь, что файл в формате PDF или DOCX.")
        else:
            await message.answer("Пожалуйста, отправьте файл с анализами в формате PDF или DOCX.")

        if not has_subscription:
            user.message_count += 1
            await session.commit()

@router.message(lambda message: message.text == "🙋‍♀️ Задать вопрос ИИ-врачу")
async def handle_question(message: types.Message, state: FSMContext):
    await state.set_state(UserState.waiting_for_question)
    await message.answer("Задайте ваш вопрос, и я постараюсь помочь.")

@router.message(UserState.waiting_for_question)
async def process_question(message: types.Message, state: FSMContext):
    async with get_session() as session:
        user = await get_or_create_user(
            session,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        )
        
        has_subscription = await check_user_subscription(session, user.id)
        
        if not has_subscription and user.message_count >= settings.FREE_MESSAGE_LIMIT:
            await message.answer(SUBSCRIPTION_MESSAGE_NOT_ENOUGH_MESSAGES)
            return
        
        response = await get_gpt_response(message.text)
        await message.answer(response)
        
        if not has_subscription:
            user.message_count += 1
            await session.commit()

@router.message(lambda message: message.text == "💊 Узнать про лекарство")
async def handle_medicine(message: types.Message, state: FSMContext):
    await state.set_state(UserState.waiting_for_medicine)
    await message.answer("О каком лекарстве вы хотели бы узнать?")

@router.message(UserState.waiting_for_medicine)
async def process_medicine(message: types.Message, state: FSMContext):
    async with get_session() as session:
        user = await get_or_create_user(
            session,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        )
        
        has_subscription = await check_user_subscription(session, user.id)
        
        if not has_subscription and user.message_count >= settings.FREE_MESSAGE_LIMIT:
            await message.answer(SUBSCRIPTION_MESSAGE_NOT_ENOUGH_MESSAGES)
            return
        
        response = await get_gpt_response(
            message.text,
            context="Ты - опытный фармацевт, который консультирует по лекарственным препаратам."
        )
        await message.answer(response)
        
        if not has_subscription:
            user.message_count += 1
            await session.commit()

@router.message(lambda message: message.text == "🩸 Женская консультация")
async def handle_female_consultation(message: types.Message, state: FSMContext):
    await state.set_state(UserState.waiting_for_female_consultation)
    await message.answer("Я готов ответить на ваши вопросы по женскому здоровью. Что вас интересует?")

@router.message(UserState.waiting_for_female_consultation)
async def process_female_consultation(message: types.Message, state: FSMContext):
    async with get_session() as session:
        user = await get_or_create_user(
            session,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        )
        
        has_subscription = await check_user_subscription(session, user.id)
        
        if not has_subscription and user.message_count >= settings.FREE_MESSAGE_LIMIT:
            await message.answer(SUBSCRIPTION_MESSAGE_NOT_ENOUGH_MESSAGES)
            return
        
        response = await get_gpt_response(message.text, is_female_consultation=True)
        await message.answer(response)
        
        if not has_subscription:
            user.message_count += 1
            await session.commit() 