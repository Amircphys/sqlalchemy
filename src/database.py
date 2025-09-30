from sqlalchemy import create_engine
from .config import settings

engine = create_engine(
    url=settings.database_url,
    echo=False,
    pool_size=5,
    max_overflow=10,
)