from typing import TYPE_CHECKING, Optional, List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy import String 
from sqlalchemy.orm import relationship
from .base import Base

if TYPE_CHECKING:
    from .address import Address



class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    username: Mapped[str | None] = mapped_column(String(20))
    addresses: Mapped[list["Address"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __str__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, username={self.username!r})"
    
    def __repr__(self) -> str:
        return str(self)