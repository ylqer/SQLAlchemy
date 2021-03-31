from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)

with Session(engine) as session:
    result = session.execute(
        text("update some_table set x = :x where y = :y"),
        [
            {"x": 999, "y": 111},
            {"x": 991, "y": 199}
        ]
    )
    session.commit()
