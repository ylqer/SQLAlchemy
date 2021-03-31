from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)

with engine.connect() as conn:
    result = conn.execute(
        text("insert into some_table (x, y) values (:x, :y)"),
        [
            {"x": 111, "y": 111},
            {"x": 222, "y": 222}
        ]
    )
    conn.commit()
    print(result)
