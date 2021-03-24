from sqlalchemy.orm import Session
from sqlalchemy import text, create_engine

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)

stmt = text("select x, y from some_table where y > :y order by x, y").bindparams(y=6)
with Session(engine) as session:
    result = session.execute(stmt)
    for row in result:
        print(f"x: {row.x}, y: {row.y}")
