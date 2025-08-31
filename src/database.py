import asyncio
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import create_engine, text, String
from config import settings
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


engine_sync = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

engine_async = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False,
    pool_size=5,
    max_overflow=10,
)


async def get_123():
    async with engine_async.connect() as conn:
        res = await conn.execute(text("SELECT VERSION()"))
        print(f"res = {res.all()}")


# asyncio.run(get_123())

session_factory_sync = sessionmaker(engine_sync)
session_factory_async = async_sessionmaker(engine_async)

# with session_sync as session:
#     ...

# async with session_async as session:
#     await session.


str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256)}
