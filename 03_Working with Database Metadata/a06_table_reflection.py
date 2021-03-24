from sqlalchemy import Table, create_engine, MetaData

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python")
metadata = MetaData()

some_table = Table("some_table", metadata, autoload_with=engine)

# some_table
# print(some_table)
