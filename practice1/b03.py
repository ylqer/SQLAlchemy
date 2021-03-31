from sqlalchemy import create_engine, text

engine = create_engine('mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python', echo=True, future=True)

with engine.begin() as conn:
    conn.execute(
        text("insert into some_table (x, y) values (:x, :y)"),
        [
            {"x": 199, "y": 199},
            {"x": 299, "y": 299}
        ]
    )
