from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1/python", echo=True, future=True)

stmt = text("select x, y from some_table where y > :y order by x, y").bindparams(y=6)
with engine.connect() as conn:
    result = conn.execute(stmt)
    for row in result:
        print(f"x: {row.x}, y: {row.y}")
