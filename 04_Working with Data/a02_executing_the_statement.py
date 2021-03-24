from sqlalchemy import create_engine, insert, MetaData, Table, Column, Integer, String

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)
metadata = MetaData()

user_table = Table(
    "user_account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(50))
)
stmt = insert(user_table).values(name='spongebob', fullname="Spongebob Squarepants")

with engine.connect() as conn:
    result = conn.execute(stmt)
    print(result.inserted_primary_key)
    conn.commit()
