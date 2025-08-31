from sqlalchemy import create_engine, text, insert
from models import metadata_obj, WorkersORM
from database import (
    engine_sync,
    engine_async,
    session_factory_sync,
    session_factory_async,
)


def create_tables():
    engine_sync.echo = True
    metadata_obj.drop_all(engine_sync)
    metadata_obj.create_all(engine_sync)
    engine_sync.echo = False


# def insert_data():
#     worker_bobr = WorkersORM(username="Bobr")
#     worker_volk = WorkersORM(username="Volk")
#     with session_factory_sync() as session:
#         session.add_all([worker_bobr, worker_volk])
#         session.commit()


async def insert_data():
    worker_bobr = WorkersORM(username="Bobr")
    worker_volk = WorkersORM(username="Volk")
    async with session_factory_async() as session:
        session.add_all([worker_bobr, worker_volk])
        await session.commit()
