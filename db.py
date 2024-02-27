import databases
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:123456@localhost:5432/currency"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

database = databases.Database(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()



