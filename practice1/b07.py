from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)

stmt = text("select * from some_table where x > :x").bindparams(x=10)
with engine.connect() as conn:
    result = conn.execute(stmt)
    for row in result:
        print(f"x: {row.x}, y: {row.y}")
