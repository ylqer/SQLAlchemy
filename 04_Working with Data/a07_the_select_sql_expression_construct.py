from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, select, create_engine

metadata = MetaData()
engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)

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
stmt = select(user_table).where(user_table.c.name == 'spongebob')
print(stmt)
with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)
