from sqlalchemy import Table, Column, String, Integer, ForeignKey, create_engine
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


# instance of classes represent rows
squidward = User(name="squidward", fullname="Squidward Tentacles")
krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")
print(squidward)

# adding objects to a session
print("*" * 150)
session = Session(engine)
session.add(squidward)
session.add(krabs)
print(session.new)

# flushing
print("*" * 150)
session.flush()

# autogenerated primary key attributes
print(squidward.id)
print(krabs.id)

# identity map
some_squidward = session.get(User, 4)
print(some_squidward)
print(some_squidward is squidward)

# committing
session.commit()