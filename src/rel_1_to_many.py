from sqlalchemy import String, Integer, ForeignKey, Column
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .database import engine

### Models
#_____________

class BaseModel(DeclarativeBase):
    __abstract__ = True 
    __allow_unmapped__ = True
    
    
class Address(BaseModel):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str]
    state: Mapped[str]
    zip_code: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    # back_populates создает двустороннюю связь, позволяя удобно перемещаться между связанными 
    # объектами в обе стороны с автоматической синхронизацией.  
    user: Mapped["User"] = relationship(back_populates="address") 
    
    def __repr__(self):
        return f"<Address(id: {self.id}, city: {self.city})>"


class User(BaseModel): 
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    address: Mapped[list['Address']] = relationship()
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, age={self.age!r}, address: {self.address})"
    
    
### Code
#______________________________________________________________________________________________________

def main():
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    
    user_dazy = User(name="Dazy Domerg", age=33)
    user_markus = User(name="Markus Woron", age=45)
    
    address_1 = Address(city="Orlean", state="Texas", zip_code="1001")
    address_2 = Address(city="Gillette", state="Wyoming", zip_code="2001")
    address_3 = Address(city="Newcastle", state="Wyoming", zip_code="2002")
    
    user_dazy.address.append(address_1)
    user_markus.address.extend([address_2, address_3])
    
    
    session.add_all([user_dazy, user_markus, address_1, address_2, address_3])
    
    # Коммитим изменения, чтобы получить ID из базы
    session.commit()
    
    print(f"user_dazy: {user_dazy}")
    print(f"user_markus: {user_markus}")
    print(f"address_3.user: {address_3.user}")
    
    
if __name__ == "__main__":
    main()