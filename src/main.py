from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from src.config import settings

engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

class Base(DeclarativeBase):
    pass 

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    username: Mapped[str | None] = mapped_column(String(20))
    addresses: Mapped[list["Address"]] = relationship(
        back_populates="users",
        cascade="all, delete-orphan",
    )
    
    def __str__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, username={self.username!r})"
    
    def __repr__(self) -> str:
        return str(self)
    
class Address(Base):
    __tablename__ = "addresses"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(20))
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
    
    
def main():
    Base.metadata.create_all(bind=engine)
    
if __name__ == "__main__":
    main() 