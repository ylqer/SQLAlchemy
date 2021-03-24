from sqlalchemy import text, create_engine

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)

# begin()没有异常自动提交，有异常则rollback
# 被称为"begin once" style
with engine.begin() as conn:
    conn.execute(
        text("insert into some_table (x, y) values (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
    )
