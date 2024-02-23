from fastapi import APIRouter

from currency import currency


routes = APIRouter()

routes.include_router(currency.router, prefix='/currency')