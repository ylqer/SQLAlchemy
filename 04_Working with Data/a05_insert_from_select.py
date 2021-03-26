from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, insert, ForeignKey
from typing import Callable

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1/python", echo=True, future=True)
metadata = MetaData()


# class ATable(Table):
#     c: Callable
#     id: Callable


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

select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
insert_stmt = insert(address_table).from_select(
    ['user_id', 'email_address'], select_stmt
)
print(insert_stmt)
