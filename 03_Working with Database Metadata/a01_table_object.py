from sqlalchemy import MetaData, Table, Column, String, Integer, create_engine

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)

metadata = MetaData()

user_table = Table(
    "user_account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String)
)


# from 01_table_object import user_table
print(user_table.c.name)
print(user_table.c.keys())
print(user_table.primary_key)
