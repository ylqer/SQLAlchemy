from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine, insert

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)
metadata = MetaData()

user_table = Table(
    "user_account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(50))
)

with engine.connect() as conn:
    conn.execute(
        insert(user_table),
        [
            # {"name": "zhiqing", "fullname": "songzhiqing"},
            # {"name": "lianjie", "fullname": "lilianjie"}
            {"name": "dehua", "fullname": "liudehua"},
            {"name": "runfa", "fullname": "zhourunfa"}
        ]
    )
    conn.commit()
