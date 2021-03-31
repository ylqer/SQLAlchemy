from sqlalchemy import Table, Integer, Column, String, MetaData, create_engine

metadata = MetaData()

user_table = Table(
    "user_account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(50))
)

print(user_table.c.name)
print(user_table.c.keys())
print(user_table.primary_key)
