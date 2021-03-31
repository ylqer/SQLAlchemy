from sqlalchemy import Table, Integer, String, MetaData, Column, insert

metadata = MetaData()

user_table = Table(
    "user_account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(50))
)

stmt = insert(user_table).values(name="路强", fullname="余路强")
print(stmt)
compiled = stmt.compile()
print(compiled.params)
