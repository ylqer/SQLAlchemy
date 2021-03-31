from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine, MetaData, select, and_, or_, func, desc
from sqlalchemy.orm import relationship, declarative_base, Session, aliased
from sqlalchemy.dialects import oracle, postgresql, mysql

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)
metadata = MetaData(0)
Base = declarative_base()

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
    Column("user_id", Integer, ForeignKey("user_account.id")),
    Column("email_address", String(50))
)


class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String(50))

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_account.id"))
    email_address = Column(String(50))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id}, user_id={self.user_id}, email_address={self.email_address})"


stmt = select(User).where(User.name == "zhiqing")
with Session(engine) as session:
    result = session.execute(stmt)
    for row in result:
        print(row)

print(select(user_table))
print(select(user_table.c.name, user_table.c.fullname))

print(select(User))
row = session.execute(select(User)).first()
print(row[0])
print(select(User.name, User.fullname))
row = session.execute(select(User.name, User.fullname)).first()
print(row)
row = session.execute(
    select(User.name, Address).
    where(User.id == Address.user_id).
    order_by(Address.user_id)
).all()
print(row)

print("*" * 150)
stmt = (
    select(("Username: " + user_table.c.name).label("name")).
    order_by(User.name)
)
result = session.execute(stmt)
print(result)
for row in result:
    print(row)


# the where clause
print("*" * 150)
print(user_table.c.name == 'dehua')
print(address_table.c.user_id > 10)
print(select(user_table).where(user_table.c.name == 'dehua'))
print(
    select(address_table.c.email_address).
    where(user_table.c.name == 'dehua').
    where(address_table.c.user_id == user_table.c.id)
)
print(
    select(address_table.c.email_address).
    where(
        user_table.c.id == address_table.c.user_id,
        user_table.c.name == "dehua"
    )
)
print(
    select(address_table.c.email_address).
    where(
        and_(
            or_(user_table.c.name == 'dehua', user_table.c.name == 'runfa'),
            user_table.c.id == address_table.c.user_id
        )
    )
)
print(select(User).filter_by(name='dehua', fullname='liudehua'))


# explicit from clause and join
print("*" * 150)
print(user_table.c.name)
print(user_table.c.name, address_table.c.email_address)
print(
    select(user_table.c.name, address_table.c.email_address).
    join_from(user_table, address_table)
)
print(
    select(user_table.c.name, address_table.c.email_address).
    join(address_table)
)
print(
    select(user_table.c.name, address_table.c.email_address).
    join(user_table)
)
print(
    select(address_table.c.email_address).
    select_from(user_table).join(address_table)
)
print(
    select(address_table.c.email_address).
    select_from(address_table).join(user_table)
)
print(
    select(func.count("*")).
    select_from(user_table)
)


# setting the on clause
print("*" * 150)
print(
    select(address_table.c.email_address).
    select_from(user_table).
    join(address_table, user_table.c.id == address_table.c.user_id)
)


# outer and full join
print("*" * 150)
print(select(user_table).join(address_table, isouter=True))
print(select(user_table).outerjoin(address_table))
print(select(user_table).join(address_table, full=True))


# order_by
print("*" * 150)
print(select(user_table).order_by(user_table.c.id))
print(select(User).order_by(User.id.asc(), User.name.desc()))


# aggregate functions with group by/having
print("*" * 150)
count_fn = func.count(user_table.c.id)
print(count_fn)
with Session(engine) as session:
    result = session.execute(
        select(User.name, func.count(Address.id).label("count")).
        join(Address).
        group_by(User.name).
        having(func.count(Address.id) >= 1)
    )
    for row in result:
        print(row)


# ordering or grouping by a label
print("*" * 150)
stmt = select(
    Address.user_id,
    func.count(Address.id).label("num_address")
).group_by(
    "user_id"
).order_by(
    "user_id", desc("num_address")
)
print(stmt)


# using aliases
print("*" * 150)
user_alias1 = user_table.alias()
user_alias2 = user_table.alias()
stmt = select(
    user_alias1.c.name, user_alias2.c.name
).join_from(user_alias1, user_alias2, user_alias1.c.id > user_alias2.c.id)
print(stmt)


# orm entity aliases
address_alias1 = aliased(Address)
address_alias2 = aliased(Address)
stmt = select(User).join_from(User, address_alias1).where(address_alias1.email_address == "dehua.liu@aol.com").join_from(User, address_alias2).where(address_alias2.email_address == "runfa.zhou@aol.com")
print(stmt)


# subquery and ctes
print("*" * 150)
subq = select(
    func.count(address_table.c.id).label("count"),
    address_table.c.user_id
).group_by(address_table.c.id).subquery()
print(subq)
print(select(subq.c.count, subq.c.user_id))
stmt = select(
    user_table.c.name,
    user_table.c.fullname,
    subq.c.count
).join_from(user_table, subq)
print(stmt)
