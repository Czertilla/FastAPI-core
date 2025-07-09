from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
import asyncio

from core.utils.settings import Settings

settings = Settings()

def get_engine(db_name: str = settings.DB_NAME) -> AsyncEngine:
    return create_async_engine(f"sqlite+aiosqlite:///{db_name}.db")

engine = get_engine()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


if __name__ == "__main__":
    from database import Base

    asyncio.run(create_tables())
