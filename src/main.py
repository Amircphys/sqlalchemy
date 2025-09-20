from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.config import settings
from src.models import Base, User, Address 


engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

def create_user(session: Session, name: str, username: str):
    user = User(
        name=name,
        username=username
    )
    session.add(user)
    session.commit()
    
def main():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        create_user(session, "Bob", 'Bob Marly')
        
        
    
if __name__ == "__main__":
    main() 