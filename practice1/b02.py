from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)

with engine.connect() as conn:
    conn.execute(
        text("create table tabletable (x int, y int)")
    )
    conn.commit()
