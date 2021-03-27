from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, select, Table, MetaData, func, cast, and_, or_, desc, JSON
from sqlalchemy.orm import Session, declarative_base, relationship, aliased
from sqlalchemy.dialects import postgresql, oracle

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


stmt = select(User).where(User.name == 'spongebob')
with Session(engine) as session:
    result = session.execute(stmt)
    print(result)
    for row in result:
        print(row)


# setting the columns and from clause
print(select(user_table))
print(select(user_table.c.name, user_table.c.fullname))


# selecting ORM entities and columns
print(select(User))
row = session.execute(select(User)).first()
print(row[0])
print(select(User.name, User.fullname))
row = session.execute(select(User.name, User.fullname)).first()
print(row)
row = session.execute(
    select(User.name, Address).
    where(User.id == Address.user_id).
    order_by(Address.id)
).all()
print(row)


# selecting from labeled sql expressions
print("i" * 150)
stmt = (
    select(
        ("Username: " + user_table.c.name).label("username"),
    ).order_by(user_table.c.name)
)
with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(f"{row.username}")


# the where clause
print(user_table.c.name == 'squidward')
print(address_table.c.user_id > 10)

print(select(user_table).where(user_table.c.name == 'squidward'))
print(
    select(address_table.c.email_address).
    where(user_table.c.name == 'squidward').
    where(address_table.c.user_id == user_table.c.id)
)
print(
    select(address_table.c.email_address).
    where(
        user_table.c.name == 'squidward',
        address_table.c.user_id == user_table.c.id
    )
)
print(
    select(address_table.c.email_address).
    where(
        and_(
            or_(User.name == 'squidward', User.name == 'sandy'),
            Address.user_id == User.id
        )
    )
)
print(select(User).filter_by(name="spongebob", fullname="Spongebob Squarepants"))


# explicit from clause and join
print(select(user_table.c.name))
print(select(user_table.c.name, address_table.c.email_address))
print(
    select(user_table.c.name, address_table.c.email_address).
    join_from(user_table, address_table)
)
print(
    select(user_table.c.name, address_table.c.email_address).
    join(address_table)
)
print(
    select(address_table.c.email_address).
    select_from(user_table).join(address_table)
)
print(
    select(func.count('*')).
    select_from(user_table)
)


# setting the on clause
print(
    select(address_table.c.email_address).
    select_from(user_table).
    join(address_table, user_table.c.id == address_table.c.user_id)
)


# outer and full join
print(select(user_table).join(address_table, isouter=True))
print(select(user_table).outerjoin(address_table))
print(select(user_table).join(address_table, full=True))


# order by
print("*" * 150)
print(select(user_table).order_by(user_table.c.name))
print(select(User).order_by(User.name.asc(), User.fullname.desc()))


# aggregate functions with group by/having
print('*' * 150)
count_fn = func.count(user_table.c.id)
print(count_fn)
with engine.connect() as conn:
    result = conn.execute(
        select(User.name, func.count(Address.id).label("count")).
        join(Address).
        group_by(User.name).
        having(func.count(Address.id) >= 1)
    )
    print(result.all())


# ordering or grouping by a label
print("*" * 150)
stmt = select(
    Address.user_id,
    func.count(Address.id).label('num_address')
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
stmt = select(User).join_from(User, address_alias1).where(address_alias1.email_address == 'patrick@aol.com').join_from(User, address_alias2).where(address_alias2.email_address == "patrick@aol.com")
print(stmt)


# subquery and ctes
print("*" * 150)
subq = select(
    func.count(address_table.c.id).label("count"),
    address_table.c.user_id
).group_by(address_table.c.user_id).subquery()
print(subq)
print(select(subq.c.user_id, subq.c.count))
stmt = select(
    user_table.c.name,
    user_table.c.fullname,
    subq.c.count
).join_from(user_table, subq)
print(stmt)


# common table expressions(ctes)
print("*" * 150)
subq = select(
    func.count(address_table.c.id).label("count"),
    address_table.c.user_id
).group_by(address_table.c.user_id).cte()
stmt = select(
    user_table.c.name,
    user_table.c.fullname,
    subq.c.count
).join_from(user_table, subq)
print(stmt)


# orm entity subquerys/ctes
print("*" * 150)
subq = select(Address).where(~Address.email_address.like('%@aol.com')).subquery()
address_subq = aliased(Address, subq)
stmt = select(User, address_subq).join_from(User, address_subq).order_by(User.id, address_subq.id)
with Session(engine) as session:
    for user, address in session.execute(stmt):
        print(f"{user} {address}")

cte = select(Address).where(~Address.email_address.like('%@aol.com')).cte()
address_cte = aliased(Address, cte)
stmt = select(User, address_cte).join_from(User, address_cte).order_by(User.id, address_cte.id)
with Session(engine) as session:
    for user, address in session.execute(stmt):
        print(f"{user}, {address}")


# scalar and correlated queries
print("*" * 150)
subq = select(func.count(address_table.c.id)).where(user_table.c.id == address_table.c.user_id).scalar_subquery()
print(subq)
print(subq == 5)
stmt = select(user_table.c.name, subq.label("address_count"))
print(stmt)
# stmt = select(
#     user_table.c.name,
#     address_table.c.email_address,
#     subq.label("address_count")
# ).join_from(
#     user_table, address_table
# ).order_by(
#     user_table.c.id, address_table.c.id
# )
# print(stmt)
subq = select(func.count(address_table.c.id)).where(user_table.c.id == address_table.c.user_id).scalar_subquery().correlate(user_table)
with engine.connect() as conn:
    result = conn.execute(
        select(
            user_table.c.name,
            address_table.c.email_address,
            subq.label("address_count")
        ).join_from(user_table, address_table).
        order_by(user_table.c.id, address_table.c.id)
    )
    print(result.all())


# exists subqueries
print("*" * 150)
subq = (
    select(func.count(address_table.c.id)).
    where(user_table.c.id == address_table.c.user_id).
    group_by(address_table.c.user_id).
    having(func.count(address_table.c.id > 1))
).exists()
with engine.connect() as conn:
    result = conn.execute(
        select(user_table.c.name).where(subq)
    )
    print(result.all())
subq = (
    select(address_table.c.id).
    where(user_table.c.id == address_table.c.user_id)
).exists()
with engine.connect() as conn:
    result = conn.execute(
        select(user_table.c.name).where(~subq)
    )
    print(result.all())


# working with sql functions
print("*" * 150)
print(select(func.count()).select_from(user_table))
print(select(func.lower("A String With Much UPPERCASE")))
stmt = select(func.now())
with engine.connect() as conn:
    result = conn.execute(stmt)
    print(result.all())
print(select(func.some_crazy_function(user_table.c.name, 17)))
print(select(func.now()).compile(dialect=postgresql.dialect()))
print(select(func.now()).compile(dialect=oracle.dialect()))


# function have return types
print("*" * 150)
print(func.now().type)
function_expr =func.json_object('{a, 1, b, "def", c, 3.5}', type_=JSON)
stmt = select(function_expr["def"])
print(stmt)


# build-in functions have pre-configured return types
print("*" * 150)
m1 = func.max(Column("some_int", Integer))
print(m1.type)
m2 = func.max(Column("some_str", String))
print(m2.type)
print(func.now().type)
print(func.current_date().type)
print(func.concat("x", "y").type)
print(func.upper("this").type)
print(select(func.upper("lowercase")+"suffix"))


# using window functions
print("*" * 150)
stmt = select(
    func.row_number().over(partition_by=user_table.c.name),
    user_table.c.name,
    address_table.c.email_address
).select_from(user_table).join(address_table)
with engine.connect() as conn:
    result = conn.execute(stmt)
    print(result.all())
stmt = select(
    func.count().over(order_by=user_table.c.name),
    user_table.c.name,
    address_table.c.email_address
).select_from(user_table).join(address_table)
with engine.connect() as conn:
    result = conn.execute(stmt)
    print(result.all())


# special modifiers within group filter
print("*" * 150)
print(
    func.unnest(
        func.percentile_disc([0.25, 0.5, 0.75, 1]).within_group(user_table.c.name)
    )
)
# stmt = select(
#     func.count(address_table.c.email_address).filter(user_table.c.name == 'sandy'),
#     func.count(address_table.c.email_address).filter(user_table.c.name == 'spongebob')
# ).select_from(user_table).join(address_table)
# with engine.connect() as conn:
#     result = conn.execute(stmt)
#     print(result.all())


# table-valued function
print("*" * 150)
# onetwothree = func.json_each('["one", "two", "three"]').table_valued("value")
# stmt = select(onetwothree).where(onetwothree.c.value.in_(["two", "three"]))
# with engine.connect() as conn:
#     result = conn.execute(stmt)
#     print(result.all())


# column valued functions - table valued function as a scalar column
# supported by postgresql and oracle
# stmt = select(func.json_array_elements('["one", "two"]')).column_valued("x")
# print(stmt)
stmt = select(func.scalar_string(5).column_valued("s"))
print(stmt.compile(dialect=oracle.dialect()))
