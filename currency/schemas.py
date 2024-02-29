from datetime import datetime
from typing import Dict

from pydantic import BaseModel, Field


class CurrencyDateTimeOut(BaseModel):
    date_and_time: datetime = Field(description="Date and time", example="2024-02-27T22:21:40.239644")

    class Config:
        from_attributes = True

