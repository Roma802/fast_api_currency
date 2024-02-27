from datetime import datetime
from typing import Dict

from pydantic import BaseModel


class CurrencyTimeStampOut(BaseModel):
    date_and_time: datetime

    class Config:
        from_attributes = True
