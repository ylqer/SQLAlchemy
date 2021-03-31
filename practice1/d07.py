from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, insert, select, create_engine

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)
metadata = MetaData()

user_table = Table(
    "user_account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(50))
)

stmt = select(user_table).where(user_table.c.name == "dehua")
with engine.connect() as conn:
    result = conn.execute(stmt)
    # print(list(result))
    for row in result:
        print(row)
