from typing import Union

from fastapi import APIRouter, Query
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.exc import NoResultFound

from db import database
from .schemas import CurrencyDateTimeOut
from .services import create_or_update_rates, get_rates, get_ratio_coefficient, get_response_for_last_datetime

router = APIRouter()


@router.put("/update-rates", tags=["currency"])
async def update_rates(base: str = 'EUR', symbols: str = ''):
    data = await get_rates(base, symbols)
    if data and data.get("success"):
        rates = data.get("rates")
        return await create_or_update_rates(rates)
    else:
        return data


@router.get("/get_last_update_datetime", tags=["currency"])
async def get_last_update_datetime():
    return await get_response_for_last_datetime()


@router.get("/get_convertible_amount", tags=["currency"])
async def get_convertible_amount(original_currency: str,
                                 target_currency: str,
                                 amount: int = Query(gt=0)) -> Union[float, dict]:
    ratio_coefficient_dict = await get_ratio_coefficient(original_currency, target_currency)
    if ratio_coefficient_dict['status'] == 'success':
        ratio_coefficient_dict['data'] = ratio_coefficient_dict['data'] * amount
    return ratio_coefficient_dict
