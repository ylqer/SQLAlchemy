from sqlalchemy import text
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:tuttidata@TT2020@127.0.0.1:3306/python", future=True, echo=True)

# 这个语句执行完后，数据库会自动rollback，而不会提交
with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())
