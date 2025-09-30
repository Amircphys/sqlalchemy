from typing import Type
import random
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_, not_
from sqlalchemy import func 
from .models import Base, User
from .database import engine

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

session = Session()

def add_users(session):
    user_john = User(name="John Conory", age=17)
    user_dazy = User(name="Dazy Domerg", age=33)
    user_markus = User(name="Markus Woron", age=45)
    user_dzho = User(name="Dzho Gage", age=42)
    user_criss = User(name="Criss Meniks", age=28)
    session.add_all([user_john, user_dazy, user_markus, user_dzho, user_criss])
    session.commit()
    
def add_random_users(session):
    names = ["John Conory", "Dazy Domergu", "Markus Woron", "Dzho Gage", "Criss Meniks"]
    ages = [35, 51, 23, 34, 28, 41, 39, 36, 25]
    for _ in range(20):
        user = User(name = random.choice(names), age = random.choice(ages))
        session.add(user)
    session.commit()

def main():
    #first!!!:
    # add_users(session)
    # users = session.query(User).filter_by(age=35).all()
    # for user in users:
    #     print(user)
    
    #second!!!: 
    # add_random_users(session=session)
    # users = session.query(User).order_by(User.age.desc(), User.name).all()
    # for user in users:
    #     print(user)
    
    #third!!!:
    # add_random_users(session=session)
    # and
    # users = session.query(User).filter(User.age > 25, User.name=='Markus Woron').all()
    # users = session.query(User).where(and_(User.age > 25, User.name=='Markus Woron')).all()
    # users = session.query(User).where((User.age > 25) & (User.name=='Markus Woron')).all()
    # users = session.query(User).where(User.age > 25, User.name=='Markus Woron').all()
    
    # or
    # users = session.query(User).where(or_(User.age > 25, User.name=='Markus Woron')).all()
    # users = session.query(User).where((User.age > 25) | (User.name=='Markus Woron')).all()
    
    # not
    # users = session.query(User).where(not_(User.age == 25)).all()
    # users = (
    #     session.query(User).where(
    #         not_(
    #             User.name == "Dazy Domergu"
    #         ),
    #         and_(
    #             User.age > 35,
    #             User.age < 50,
    #         )
    #     )
    # )


    #fourth!!!:
    # add_random_users(session=session)
    # group
    
    # users = session.query(User.name, func.count(User.id)).group_by(User.name).all()
    # users = (
    #     session.query(User.age, func.count(User.name))
    #     .filter(User.age>24)
    #     .order_by(User.age)
    #     .filter(User.age<50)
    #     .group_by(User.age)
    #     .all()
        
    # )
    # only_criss = True
    # group_by_age = True
    # users = session.query(User)
    # if only_criss:
    #     users = users.filter(User.name == "Criss Meniks")
    # if group_by_age:
    #     users = users.group_by(User.age)
    # users = users.all()
    # for user in users:
    #     print(user)
        
    pass
    
    
    
    
if __name__ == "__main__":
    main()