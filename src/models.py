from typing import Optional, Annotated
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base, str_256
import enum
import datetime


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    ),
]


## Declarative style
class WorkersORM(Base):
    __tablename__ = "workers"
    id: Mapped[intpk]
    username: Mapped[str]


class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class ResumeORM(Base):
    __tablename__ = "resume"
    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[int | None]  # Mapped[int] = mapped_column(nullable=True)
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(
        ForeignKey("workers.id", ondelete="CASCADE")
    )  # ondelete="SET NULL"
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


## Imperative style
metadata_obj = MetaData()

workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)
