import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import create_engine, text, insert
from config import settings
from models import metadata_obj, workers_table


engine_sync = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
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


def create_tables():
    engine_sync.echo = True
    metadata_obj.drop_all(engine_sync)
    metadata_obj.create_all(engine_sync)
    engine_sync.echo = False


def insert_data():
    print(f"Insert data function...")
    with engine_sync.connect() as conn:
        # stmt = """
        #     INSERT INTO workers (username) VALUES
        #     ('AO Bobr'),
        #     ('OOO Volk');
        # """
        stmt = insert(workers_table).values(
            [
                {"username": "AO Bobr"},
                {"username": "OOO Volk"},
            ]
        )
        conn.execute(stmt)
        conn.commit()
