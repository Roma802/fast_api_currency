from typing import Union

from fastapi import APIRouter, Query
from sqlalchemy import text

from db import database
from .schemas import CurrencyTimeStampOut
from .services import create_or_update_rates, get_rates, get_ratio_coefficient

router = APIRouter()


@router.put("/update-rates", tags=["currency"])
async def update_rates(base: str = 'EUR', symbols: str = '') -> dict:
    data = await get_rates(base, symbols)
    if data and data.get("success"):
        rates = data.get("rates")
        return await create_or_update_rates(rates)
    else:
        return {"message": "Failed to update rates"}


@router.get("/get_last_update_datetime", tags=["currency"], response_model=CurrencyTimeStampOut)
async def get_last_update_datetime():
    last_datetime_update = await database.execute(text("SELECT MAX(date_and_time) FROM currency"))
    return CurrencyTimeStampOut(date_and_time=last_datetime_update)


@router.get("/get_convertible_amount", tags=["currency"])
async def get_convertible_amount(original_currency: str,
                                 target_currency: str,
                                 amount: int = Query(gt=0)) -> Union[float, dict]:
    ratio_coefficient = await get_ratio_coefficient(original_currency, target_currency)
    if ratio_coefficient:
        return ratio_coefficient * amount
    else:
        return {"message": "Failed to get convertible amount"}
