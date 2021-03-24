# from sqlalchemy.orm import registry

# mapper_registry = registry()
# Base = mapper_registry.generate_base()

# print(mapper_registry.metadata)

# 以上创建Base的语句可以简化为下面这两句
from sqlalchemy.orm import declarative_base
Base = declarative_base()

