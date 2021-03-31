from sqlalchemy import Table, MetaData, create_engine

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)
metadata = MetaData()

some_table = Table("some_table", metadata, autoload_with=engine)

print(some_table.c.keys())
# print(some_table.c.name())
print(some_table.primary_key)
