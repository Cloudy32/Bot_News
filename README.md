# Telegram News Sorter Bot (Aiogram)

Бот собирает новости из RSS-источников, хранит их в SQLite, принимает интересы пользователя и выдаёт топ-5 самых релевантных и свежих новостей.

## Возможности

- Парсинг новостей (по умолчанию: Lenta, RBC, RIA)
- Сохранение в SQLite (`news.db`)
- Поиск похожих новостей по эмбеддингам (`sentence-transformers`)
- Ранжирование: релевантность + свежесть
- Команда `/update` для ручного обновления базы
- Ответ: заголовок, краткое описание, ссылка

## Технологии

- `aiogram` 3.x
- `SQLite` + `aiosqlite` + `SQLAlchemy` (async ORM)
- `feedparser`
- `sentence-transformers`

## Быстрый старт (Windows / PowerShell)

1. Установи Python 3.11+.
2. Перейди в папку проекта:

```bash
cd C:\Users\user\news_sorter_bot
```

3. Создай и активируй виртуальное окружение:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Установи зависимости:

```bash
pip install -r requirements.txt
```

5. Создай `.env` на основе примера:

```bash
copy .env.example .env
```

6. Заполни `.env`:

```env
BOT_TOKEN=your_telegram_bot_token
DB_PATH=news.db
```

7. Запусти бота:

```bash
python bot.py
```

## Использование

- `/start` - подсказка по командам
- `/update` - загрузить свежие новости
- Просто текстом: `спорт и ИИ` - получить топ-5

## Настройка источников

Измени словарь `NEWS_FEEDS` в `fetcher.py`, добавь или убери RSS-ленты.
