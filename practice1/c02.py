from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, create_engine

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python")
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
    Column("user_id", Integer, ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String(50), nullable=False)
)

# metadata.drop_all(engine)
metadata.create_all(engine)
# print(address_table.c.keys())
