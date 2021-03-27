from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, update, bindparam, select, delete
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects import mysql


engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)
metadata = MetaData()

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String(50))

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


user_table = Table(
    "user_account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(50))
)


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_account.id"))
    email_address = Column(String(50))

    user = relationship("User", back_populates="addresses")


address_table = Table(
    "address",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String(50), nullable=False)
)

some_table1 = Table(
    "some_table",
    metadata,
    Column("x", Integer),
    Column("y", Integer)
)

# the update sql expression construct
stmt = (
    update(user_table).where(user_table.c.name == 'patrick').
    values(fullname="Patrick the Star")
)
print(stmt)
stmt = (
    update(user_table).
    values(fullname="Username: " + user_table.c.name)
)
print(stmt)
stmt = (
    update(user_table).
    where(user_table.c.name == bindparam('oldname')).
    values(name=bindparam('newname'))
)
with engine.begin() as conn:
    conn.execute(
        stmt,
        [
            {'oldname': 'jack', 'newname': 'ed'},
            {'oldname': 'wendy', 'newname': 'mary'},
            {'oldname': 'jim', 'newname': 'jake'}
        ]
    )

# correlated updates
scalar_subq = (
    select(address_table.c.email_address).
    where(address_table.c.user_id == user_table.c.id).
    order_by(user_table.c.id).
    limit(1).
    scalar_subquery()
)
update_stmt = update(user_table).values(fullname=scalar_subq)
print(update_stmt)

# update...from
print("*" * 150)
update_stmt = (
    update(user_table).
    where(user_table.c.id == address_table.c.user_id).
    where(address_table.c.email_address == "patrick@aol.com").
    values(fullname="Pat")
)
print(update_stmt)
update_stmt = (
    update(user_table).
    where(user_table.c.id == address_table.c.user_id).
    where(address_table.c.email_address == "patrick@aol.com").
    values(
        {
            user_table.c.fullname: "Pat",
            address_table.c.email_address: "pat@aol.com"
        }
    )
)
print(update_stmt.compile(dialect=mysql.dialect()))

# parameter ordered updates
# print("*" * 150)
# update_stmt = (
#     update(user_table).
#     ordered_values(
#         (some_table1.c.y, 20),
#         (some_table1.c.x, some_table1.c.y + 10)
#     )
# )
# print(update_stmt)


# the delete sql expression construct
print("*" * 150)
stmt = delete(user_table).where(user_table.c.name == "patrick")
print(stmt)


# multiple table deletes
print("*" * 150)
delete_stmt = (
    delete(user_table).
    where(user_table.c.id == address_table.c.user_id).
    where(address_table.c.email_address == "patrick@aol.com")
)
print(delete_stmt.compile(dialect=mysql.dialect()))


# getting affected row count from update and delete
print("*" * 150)
with engine.begin() as conn:
    result = conn.execute(
        update(user_table).
        values(fullname="Patrick McStar").
        where(user_table.c.name == "patrick")
    )
    print(result.rowcount)


# using returing with delete update
print("*" * 150)
update_stmt = (
    update(user_table).where(user_table.c.name == "patrick").values(fullname="Patrick the Star").
    returning(user_table.c.id, user_table.c.name)
)
print(update_stmt)
delete_stmt = (
    delete(user_table).where(user_table.c.name == "patrick").
    returning(user_table.c.id, user_table.c.name)
)
print(delete_stmt)
