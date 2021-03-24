from sqlalchemy import text, create_engine

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)

with engine.connect() as conn:
    conn.execute(text("create table some_table (x int, y int)"))
    conn.execute(
        text("insert into some_table (x, y) values (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
    )
    # create_engine中加入future才会有commit命令，否则没有,并且还会自动提交
    # 创建表的命令不会被rollback
    # 被称为"commit as you go" style
    conn.commit()
