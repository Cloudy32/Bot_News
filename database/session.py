from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from database.models import Base


def make_engine(db_path: str) -> AsyncEngine:
    db_url = f"sqlite+aiosqlite:///{db_path}"
    return create_async_engine(db_url, echo=False)


def make_session_factory(db_path: str) -> async_sessionmaker[AsyncSession]:
    engine = make_engine(db_path)
    return async_sessionmaker(engine, expire_on_commit=False)


async def init_db(db_path: str) -> None:
    engine = make_engine(db_path)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
