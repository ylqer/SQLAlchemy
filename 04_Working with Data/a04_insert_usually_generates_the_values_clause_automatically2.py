from sqlalchemy import create_engine, insert, MetaData, Table, Column, Integer, String, select, bindparam, ForeignKey

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)
metadata = MetaData()


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
    Column("email_address", String(50), nullable=False)
)

scalar_subquery = (
    select(user_table.c.id).
    where(user_table.c.name == bindparam('username')).
    scalar_subquery()
)
print(scalar_subquery)

with engine.connect() as conn:
    result = conn.execute(
        insert(address_table).values(user_id=scalar_subquery),
        [
            {"username": "luqiang", "email_address": "spongebob@sqlalchemy.org"},
            {"username": "zhiqing", "email_address": "sandy@sqlalchemy.org"},
            {"username": "lianjie", "email_address": "sandy@squirrelpower.org"}
        ]
    )
    conn.commit()
