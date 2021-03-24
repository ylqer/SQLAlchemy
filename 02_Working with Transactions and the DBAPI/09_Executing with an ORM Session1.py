from sqlalchemy.orm import Session
from sqlalchemy import text, create_engine

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)

with Session(engine) as session:
    result = session.execute(
        text("update some_table set y = :y where x = :x"),
        [{"x": 9, "y": 11}, {"x": 13, "y": 15}]
    )
    session.commit()
