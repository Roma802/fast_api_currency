from fastapi import FastAPI

# from routes import routes
from currency import models
from currency.routes import routes as routes1
from db import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(routes1)

