from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from database.models import News


async def save_news(
    session_factory: async_sessionmaker[AsyncSession], items: Iterable[dict]
) -> int:
    rows = [
        {
            "title": item["title"],
            "summary": item["summary"],
            "link": item["link"],
            "published_at": item["published_at"],
            "source": item["source"],
        }
        for item in items
    ]
    if not rows:
        return 0

    stmt = insert(News).values(rows).on_conflict_do_nothing(index_elements=["link"])
    async with session_factory() as session:
        result = await session.execute(stmt)
        await session.commit()
        return int(result.rowcount or 0)


async def get_all_news(session_factory: async_sessionmaker[AsyncSession]) -> list[dict]:
    async with session_factory() as session:
        result = await session.execute(select(News).order_by(News.published_at.desc()))
        rows = result.scalars().all()

    return [
        {
            "title": row.title,
            "summary": row.summary,
            "link": row.link,
            "published_at": row.published_at,
            "source": row.source,
        }
        for row in rows
    ]
