from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)

with engine.connect() as conn:
    result = conn.execute(text("select * from some_table"))
    for row in result:
        print(f"x: {row.x}, y: {row.y}")
