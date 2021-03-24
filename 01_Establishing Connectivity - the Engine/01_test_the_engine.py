from sqlalchemy import create_engine

# echo参数可以指定将数据库产生的日志输出到标准输出台
engine = create_engine("mysql+pymysql://root@tuttidata@TT2020@127.0.0.1:3306/python", echo=True, future=True)

