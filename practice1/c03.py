from sqlalchemy.orm import registry, declarative_base

mapped_registry = registry()
Base = mapped_registry.generate_base()
print(mapped_registry.metadata)

# Base = declarative_base()
