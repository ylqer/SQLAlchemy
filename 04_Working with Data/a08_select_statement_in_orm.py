from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, select
from sqlalchemy.orm import Session, declarative_base, relationship

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String(50))

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_account.id"))
    email_address = Column(String(50))

    user = relationship("User", back_populates="addresses")


stmt = select(User).where(User.name == 'spongebob')
with Session(engine) as session:
    result = session.execute(stmt)
    print(result)
    for row in result:
        print(row)
