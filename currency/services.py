import json
from datetime import datetime
from typing import Dict, List

import asyncpg
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from db import database
from . import models
from .constants import API_KEY, BASE_URL
import httpx

from .models import currency_table


async def create_or_update_rates(rates: Dict[str, float]):
    for currency_name, rate in rates.items():
        db_currency_obj = await database.fetch_one(select(models.Currency).where(models.Currency.name == currency_name))
        if db_currency_obj:
            query = currency_table.update().where(currency_table.c.name == currency_name)\
                        .values(rate=rate, date_and_time=datetime.now())
            await database.execute(query)
        else:
            db_currency_obj = currency_table.insert().values(name=currency_name, rate=rate)
            await database.execute(db_currency_obj)
    return {'message': 'Rates updated successfully', 'rates': json.dumps(rates)}


async def get_rates(base, symbols):
    try:
        async with httpx.AsyncClient() as client:
            params = {'access_key': API_KEY, 'base': base, 'symbols': symbols}
            response = await client.get(f'{BASE_URL}latest', params=params)
            return response.json()
    except httpx.RequestError as e:
        print('Ошибка при запросе к API:', e)
        return None


async def get_ratio_coefficient(original_currency: str, target_currency: str):
    try:
        last_rate_for_original_currency = await database.fetch_one(
            select(models.Currency.rate).where(models.Currency.name == original_currency)
        )
        last_rate_for_target_currency = await database.fetch_one(
            select(models.Currency.rate).where(models.Currency.name == target_currency)
        )
    except NoResultFound:
        return None
    return last_rate_for_target_currency[0] / last_rate_for_original_currency[0]
