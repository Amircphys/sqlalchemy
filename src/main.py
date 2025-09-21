from typing import List, Optional, Iterable
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.config import settings
from src.models import Base, User, Address 


engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

def create_user(session: Session, name: str, username: str, emails: Optional[List[str]]=None)-> User:    
    user = User(
        name=name,
        username=username,
        addresses=[Address(email=email) for email in emails] if emails else []
    )
    session.add(user)
    session.commit()
    return user


def fetch_user(session: Session, name: str)-> User | None:
    stmt = select(User).where(User.name == name)
    user: User | None = session.execute(stmt).scalar_one_or_none()
    return user


def add_addresses(session: Session, user: User, emails: List[str])-> None:
    user.addresses = [Address(email=email) for email in emails]
    session.commit()
    
    
def main():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        bob_user = create_user(session, "Bob", 'Bob Marly')
        john_user = create_user(session, "John", 'John Conory', ["john@example.com", "john_conory@example.com"])
        add_addresses(session, bob_user, ['bob_99@example.com'])
        user = fetch_user(session, "Bob")
        # print(f"user: {user}")
        users: Iterable[User] = session.scalars(select(User))
        for user in users:
            print(f"user: {user}")
            print(f"Emails for this user:")
            for address in user.addresses:
                print(address.email)
    
if __name__ == "__main__":
    main() 