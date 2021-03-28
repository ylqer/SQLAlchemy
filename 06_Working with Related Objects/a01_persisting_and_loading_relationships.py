from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, select, Table, MetaData, func, cast, and_, or_, desc, JSON
from sqlalchemy.orm import Session, declarative_base, relationship, aliased, selectinload, joinedload, contains_eager
from sqlalchemy.dialects import postgresql, oracle

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)
metadata = MetaData()
session = Session(engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String(50))

    addresses = relationship("Address", back_populates="user", lazy="selectin")

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


# persisting and loading relationship
u1 = User(name="pkrabs", fullname="Pearl Krabs")
print(u1.addresses)
a1 = Address(email_address="pearl.krabs@gmail.com")
u1.addresses.append(a1)
print(u1.addresses)
print(a1.user)
a2 = Address(email_address="pearl@aol.com", user=u1)
print(u1.addresses)
print(a2.user)


# cascading objects into the session
session.add(u1)
print(u1 in session)
print(a1 in session)
print(a2 in session)
print(u1.id)
print(a1.user_id)
session.commit()

# loading relationships
print(u1.id)
print(u1.addresses)
print(u1.addresses)
print(a1)
print(a2)


# using relationships in queries
# using relationships to join
print(
    select(Address.email_address).
    select_from(User).
    join(User.addresses)
)
print(
    select(Address.email_address).
    join_from(User, Address)
)

# join between aliased targets
address_alias_1 = aliased(Address)
address_alias_2 = aliased(Address)
print(
    select(User).
    join(User.addresses.of_type(address_alias_1)).
    where(address_alias_1.email_address == "patrick@aol.com").
    join(User.addresses.of_type(address_alias_2)).
    where(address_alias_2.email_address == "patrick@gmail.com")
)
user_alias_1 = aliased(User)
print(
    select(user_alias_1.name).
    join(user_alias_1.addresses)
)

# augmenting the on criteria
stmt = (
    select(User.fullname).
    join(User.addresses.and_(Address.email_address == 'pearal.krabs@gmail.com'))
)
print(session.execute(stmt).all())


# exists forms: has()/any()
stmt = (
    select(User.fullname).
    where(User.addresses.any(Address.email_address == "pearl.krabs@gmail.com"))
)
print(session.execute(stmt).all())
stmt = (
    select(User.fullname).
    where(~User.addresses.any())
)
print(session.execute(stmt).all())
stmt = (
    select(Address.email_address).
    where(Address.user.has(User.name == "pkrabs"))
)
print(session.execute(stmt).all())

# common relationship operators
print(select(Address).where(Address.user == u1))
print(select(Address).where(Address.user != u1))
print(select(User).where(User.addresses.contains(a1)))

# loader strategies
for user_obj in session.execute(
    select(User).options(selectinload(User.addresses))
).scalars():
    print(user_obj.addresses)

# selectin load
print("*" * 150)
stmt = (
    select(User).options(selectinload(User.addresses)).order_by(User.id)
)
for row in session.execute(stmt):
    print(f"{row.User.name} ({', '.join(a.email_address for a in row.User.addresses)})")

# joined load
stmt = (
    select(Address).options(joinedload(Address.user, innerjoin=True)).order_by(Address.id)
)
for row in session.execute(stmt):
    print(f"{row.Address.email_address}, {row.Address.user.name}")

# explicit join + eager load
print("*" * 150)
stmt = (
    select(Address).
    join(Address.user).
    where(User.name == "pkrabs").
    options(contains_eager(Address.user)).order_by(Address.id)
)
for row in session.execute(stmt):
    print(f"{row.Address.email_address}, {row.Address.user.name}")
stmt = (
    select(Address).
    join(Address.user).
    where(User.name == "pkrabs").
    options(joinedload(Address.user)).order_by(Address.id)
)
print(stmt)

# augmenting loader strategy paths
stmt = (
    select(User).
    options(
        selectinload(
            User.addresses.and_(
                ~Address.email_address.endswith("sqlalchemy.org")
            )
        )
    ).
    order_by(User.id).
    execution_options(populate_existing=True)
)
for row in session.execute(stmt):
    print(f"{row.User.name}  ({', '.join(a.email_address for a in row.User.addresses)})")

# raiseload



















