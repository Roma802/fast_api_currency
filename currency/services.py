import json
from datetime import datetime
from typing import Dict, List

import asyncpg
from pydantic import ValidationError
from sqlalchemy import select, text
from sqlalchemy.exc import NoResultFound

from db import database
from . import models
from .constants import API_KEY, BASE_URL
import httpx

from .models import currency_table
from .schemas import CurrencyDateTimeOut


async def create_or_update_rates(rates: Dict[str, float]):
    try:
        for currency_name, rate in rates.items():
            db_currency_obj = await database.fetch_one(select(models.Currency)
                                                       .where(models.Currency.name == currency_name))
            if db_currency_obj:
                query = currency_table.update().where(currency_table.c.name == currency_name)\
                            .values(rate=rate, date_and_time=datetime.now())
                await database.execute(query)
            else:
                db_currency_obj = currency_table.insert().values(name=currency_name, rate=rate)
                await database.execute(db_currency_obj)
    except Exception:
        return {
                "status": "error",
                "details": "Rates updated unsuccessfully",
                "data": None,
            }
    return {
                "status": "success",
                "details": "Rates updated successfully",
                "data": rates,
            }


async def get_rates(base, symbols):
    try:
        async with httpx.AsyncClient() as client:
            params = {'access_key': API_KEY, 'base': base, 'symbols': symbols}
            response = await client.get(f'{BASE_URL}latest', params=params)
            return response.json()
    except httpx.RequestError as e:
        print('Error when requesting an API:', e)
        return {
                "status": "error",
                "details": "Error when requesting an API",
                "data": None,
            }


async def get_ratio_coefficient(original_currency: str, target_currency: str):
    try:
        last_rate_for_original_currency = await database.fetch_one(
            select(models.Currency.rate).where(models.Currency.name == original_currency)
        )
        last_rate_for_target_currency = await database.fetch_one(
            select(models.Currency.rate).where(models.Currency.name == target_currency)
        )
        if not last_rate_for_target_currency or not last_rate_for_original_currency:
            raise NoResultFound
        result = last_rate_for_target_currency[0] / last_rate_for_original_currency[0]
        return {
            "status": "success",
            "details": None,
            "data": result,
        }
    except NoResultFound:
        return {
            "status": "error",
            "details": "There is no suitable result in the database",
            "data": None,
        }
    except ZeroDivisionError:
        return {
            "status": "error",
            "details": "Cannot divide by 0",
            "data": None,
        }


async def get_response_for_last_datetime():
    try:
        last_datetime_update = await database.execute(text("SELECT MAX(date_and_time) FROM currency"))
        if not last_datetime_update:
            raise NoResultFound
        return {
                "status": "success",
                "details": None,
                "data": CurrencyDateTimeOut(date_and_time=last_datetime_update),
            }
    except NoResultFound:
        return {
            "status": "error",
            "details": "There are no dates in the database",
            "data": None,
        }
    except ValidationError:
        return {
            "status": "error",
            "details": "Validation error",
            "data": None,
        }
