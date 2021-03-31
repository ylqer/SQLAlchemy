from sqlalchemy import Table, Column, Integer, String, MetaData, insert, create_engine

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)
metadata = MetaData()

user_table = Table(
    "user_account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(50))
)

stmt = insert(user_table).values(name="luqiang", fullname="yuluqiang")
with engine.connect() as conn:
    conn.execute(stmt)
    conn.commit()
