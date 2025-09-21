from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer
from .config import settings


engine = create_engine(
    url=settings.database_url,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    
    

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

