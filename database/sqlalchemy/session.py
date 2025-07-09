from core.utils.settings import getSettings
from sqlalchemy.ext.asyncio import async_sessionmaker

match ( settings := getSettings()).DB_DBMS:
    case "sqlite":
        from .sqlite import engine
    case "postgres":
        from .pgsql import engine

new_session = async_sessionmaker(engine, expire_on_commit=False)
