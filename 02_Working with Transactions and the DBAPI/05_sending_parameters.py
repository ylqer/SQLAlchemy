from sqlalchemy import text, create_engine

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1/python", echo=True, future=True)

with engine.connect() as conn:
    result = conn.execute(
        text("select * from some_table where y > :y"),
        {"y": 2}
    )
    for row in result:
        print(f"x: {row.x}, y: {row.y}")
