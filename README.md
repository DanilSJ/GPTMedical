# GPT Medical Bot 🤖

Telegram бот для медицинского анализа документов с использованием GPT и OCR технологий.

## Возможности ✨

- 📄 Анализ медицинских документов (PDF, DOCX, изображения)
- 🔍 Извлечение текста из документов с помощью OCR
- 💡 Интеллектуальный анализ с использованием GPT
- 💳 Система подписок с разными тарифами
- 📊 Отслеживание использования и лимитов
- 🔒 Безопасное хранение данных

## Технологии 🛠

- Python 3.11+
- aiogram 3.3.0
- SQLAlchemy 2.0.25
- OpenAI API
- Tesseract OCR
- PostgreSQL
- YooKassa для платежей

## Установка 🚀

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/gpt-medical-bot.git
cd gpt-medical-bot
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` и настройте переменные окружения:
```env
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
YOOKASSA_SHOP_ID=your_shop_id
YOOKASSA_SECRET_KEY=your_secret_key
```

5. Установите Tesseract OCR:
```bash
# MacOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# Скачайте установщик с https://github.com/UB-Mannheim/tesseract/wiki
```

6. Примените миграции базы данных:
```bash
alembic upgrade head
```

## Запуск 🏃‍♂️

```bash
python src/main.py
```

## Структура проекта 📁

```
gpt-medical-bot/
├── src/
│   ├── handlers/      # Обработчики команд бота
│   ├── services/      # Бизнес-логика
│   ├── models/        # Модели базы данных
│   ├── utils/         # Вспомогательные функции
│   └── main.py        # Точка входа
├── config/            # Конфигурация
├── migrations/        # Миграции базы данных
├── requirements.txt   # Зависимости
└── README.md         # Документация
```

## Тарифы 💰

- **Базовый**: 5 бесплатных запросов в день
- **Стандарт**: 50 запросов в месяц
- **Премиум**: Неограниченное количество запросов

## Безопасность 🔒

- Все документы обрабатываются локально
- Данные пользователей шифруются
- Безопасное хранение платежной информации
- Регулярное резервное копирование

## Лицензия 📄

MIT License

## Контакты 📧

Если у вас есть вопросы или предложения, создайте issue в репозитории или свяжитесь с нами. 