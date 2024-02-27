import asyncio

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

# from routes import routes
from currency import models
from currency.routes import routes as routes1
from db import engine, database, Base


# models.Base.metadata.create_all(bind=engine)

# Создаем таблицы
# async def create_tables():
#     async with AsyncEngine(engine) as conn:
#         await conn.run_sync(models.Base.metadata.create_all)
#
# create_tables()


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(routes1)

