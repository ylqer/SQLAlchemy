# 运行失败

from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)
metadata = MetaData()

Base = declarative_base()
#
# user_table = Table(
#     "user_account",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String(30)),
#     Column("fullname", String(50))
# )
#
# address_table = Table(
#     "address",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("email_address", String(50), nullable=False)
# )

user_table = Table(
    "user_account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(50))
)

address_table = Table(
    "address",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String(50), nullable=False)
)


class User(Base):
    __table__ = user_table

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"User({self.name!r}, {self.fullname!r}"


class Address(Base):
    __table__ = address_table

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address{self.email_address!r}"


Base.metadata.create_all(engine)
