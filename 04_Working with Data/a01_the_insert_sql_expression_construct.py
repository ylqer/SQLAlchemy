from sqlalchemy import insert, Table, MetaData, Column, Integer, String

metadata = MetaData()

user_table = Table(
    "user_account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(50))
)

stmt = insert(user_table).values(name='spongebob', fullname='Spongebob Squarepants')

print(stmt)
compiled = stmt.compile()
print(compiled.params)
