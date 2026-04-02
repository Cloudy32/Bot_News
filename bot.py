import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from config import load_settings
from database import get_all_news, init_db, make_session_factory, save_news
from fetcher import fetch_news
from recommender import rank_news


logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def short(text: str, max_len: int = 220) -> str:
    clean = " ".join(text.split())
    if len(clean) <= max_len:
        return clean
    return clean[: max_len - 1].rstrip() + "..."


def register_handlers(dp: Dispatcher, db_path: str) -> None:
    session_factory = make_session_factory(db_path)

    @dp.message(Command("start"))
    async def start_handler(message: Message) -> None:
        text = (
            "Привет! Я новостной сортировщик.\n\n"
            "Что умею:\n"
            "- /update - загрузить свежие новости в базу\n"
            "- Отправь интересы текстом (например: 'ИИ и криптовалюты'), и я пришлю топ-5"
        )
        await message.answer(text)

    @dp.message(Command("update"))
    async def update_handler(message: Message) -> None:
        await message.answer("Обновляю базу новостей...")
        items = fetch_news(limit_per_source=120)
        inserted = await save_news(session_factory, items)
        total = len(await get_all_news(session_factory))
        await message.answer(f"Готово. Добавлено новых: {inserted}\nВсего в базе: {total}")

    @dp.message(F.text)
    async def interests_handler(message: Message) -> None:
        query = (message.text or "").strip()
        if not query:
            await message.answer("Пришли интересы текстом.")
            return

        all_news = await get_all_news(session_factory)
        if not all_news:
            await message.answer("База пустая. Сначала вызови /update")
            return

        ranked = rank_news(query, all_news, top_k=5)
        if not ranked:
            await message.answer("Пока не нашел подходящих новостей.")
            return

        chunks = [f"Топ-5 по запросу: {query}\n"]
        for i, item in enumerate(ranked, start=1):
            chunks.append(
                f"{i}) {item['title']}\n"
                f"Источник: {item['source']}\n"
                f"Описание: {short(item['summary'])}\n"
                f"Ссылка: {item['link']}\n"
            )

        await message.answer("\n".join(chunks), disable_web_page_preview=True)


async def main() -> None:
    settings = load_settings()
    await init_db(settings.db_path)

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    register_handlers(dp, settings.db_path)

    logger.info("Aiogram bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
