from datetime import datetime
from typing import Dict

from pydantic import BaseModel


class CurrencyTimeStampOut(BaseModel):
    timestamp: datetime

    class Config:
        orm_mode = True  # это может вызвать ошибку потому что у нас метод get, а не post
