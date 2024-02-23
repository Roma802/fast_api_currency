from typing import Union

import requests
from fastapi import Depends, APIRouter, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from . import models
from .dependencies import get_db
from .schemas import CurrencyTimeStampOut
from .services import create_or_update_rates, get_rates, get_ratio_coefficient

# Нужно переделать все на АСИНХРОННЫЙ РЕЖИМ

router = APIRouter()


@router.put("/update-rates", tags=["currency"])
def update_rates(base: str = 'EUR', symbols: str = '', db: Session = Depends(get_db)) -> dict:
    data = get_rates(base, symbols)
    if data and data.get("success"):
        rates = data.get("rates")
        return create_or_update_rates(rates, db)
    else:
        return {"message": "Failed to update rates"}


@router.get("/get_last_update_datetime", tags=["currency"], response_model=CurrencyTimeStampOut)
def get_last_update_datetime(db: Session = Depends(get_db)):
    last_datetime_update = db.query(func.max(models.Currency.timestamp)).scalar()
    return CurrencyTimeStampOut(timestamp=last_datetime_update)


@router.get("/get_convertible_amount", tags=["currency"])
def get_convertible_amount(original_currency: str,  # нужно еще проверить или нужно писать ... чтобы сделать обязательными
                           target_currency: str,
                           amount: int = Query(gt=0),
                           db: Session = Depends(get_db)) -> Union[float, dict]:
    ratio_coefficient = get_ratio_coefficient(original_currency, target_currency, db)
    if ratio_coefficient:
        return ratio_coefficient * amount
    else:
        return {"message": "Failed to get convertible amount"}
