import json
from datetime import datetime
from typing import Dict, List

import requests
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from . import models
from .constants import API_KEY, BASE_URL


def create_or_update_rates(rates: Dict[str, float], db: Session):
    for currency_name, rate in rates.items():
        db_currency_obj = db.query(models.Currency).filter(models.Currency.name == currency_name).first()
        if db_currency_obj:
            db_currency_obj.rate = rate
            db_currency_obj.timestamp = datetime.utcnow()
        else:
            db_currency_obj = models.Currency(name=currency_name, rate=rate)
            db.add(db_currency_obj)
    db.commit()
    # db.refresh(db_currency_obj)
    return {'message': 'Rates updated successfully', 'rates': json.dumps(rates)}


def get_rates(base, symbols):
    try:
        params = {'access_key': API_KEY, 'base': base, 'symbols': symbols}
        response = requests.get(f'{BASE_URL}latest', params=params)
        # response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print('Ошибка при запросе к API:', e)
        return None


def get_ratio_coefficient(original_currency: str, target_currency: str, db: Session):
    try:
        last_rate_for_original_currency = db.query(models.Currency.rate).filter(models.Currency.name == original_currency).first()
        last_rate_for_target_currency = db.query(models.Currency.rate).filter(models.Currency.name == target_currency).first()
    except NoResultFound:
        return None
    return last_rate_for_original_currency[0] / last_rate_for_target_currency[0]
