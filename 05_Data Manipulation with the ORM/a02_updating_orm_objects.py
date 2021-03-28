from sqlalchemy import Table, Column, String, Integer, ForeignKey, create_engine, select, update
from sqlalchemy.orm import declarative_base, registry, relationship, Session

# mapper_registry = registry()
# Base = mapper_registry.generate_base()
# print(mapper_registry.metadata)
Base = declarative_base()
engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)


class User(Base):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String(50))

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_account.id"))
    email_address = Column(String(50))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id}, user_id={self.user_id}, email_address={self.email_address})"


session = Session(engine)
sandy = session.execute(select(User).filter_by(name="sandy")).scalar_one()
print(sandy)
sandy.fullname = "Sandy Squirrel"
print(sandy in session.dirty)
sandy_fullname = session.execute(
    select(User.fullname).where(User.id == 3)
).scalar_one()
print(sandy_fullname)
print(sandy in session.dirty)

# orm-enabled update statements
session.execute(
    update(User).
    where(User.name == "sandy").
    values(fullname="Sandy Squirrel Extraodinaire")
)
print(sandy.fullname)